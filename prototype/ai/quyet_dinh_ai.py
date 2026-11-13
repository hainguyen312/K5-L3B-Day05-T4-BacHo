"""Lời gọi AI thật cho quyết định chính của lát cắt T4 (bonus +3).

AI đọc khiếu nại "không đúng mô tả", so với MÔ TẢ LÚC ĐẶT, rồi chọn MỘT bước tiếp theo:
hướng dẫn gửi yêu cầu trả hàng / xin thêm bằng chứng / chuyển nhân viên.

Mức tự chủ ở spec.md §4 được khoá bằng code, không chỉ bằng prompt:
- Schema đầu ra chỉ có 3 bước trên. AI không thể trả về "hoàn tiền", "từ chối" hay "phạt shop".
- Sau khi nhận kết quả, code kiểm thêm các luật cứng (không hứa kết quả, không lấy lời doạ
  hay lịch sử làm căn cứ) và ghi vi phạm vào log nếu có.

Chỉ dùng dữ liệu dựng (README: không đưa dữ liệu thật vào công cụ AI).
Model: OpenAI gpt-4.1-mini, Structured Outputs (json_schema, strict) để khoá 3 bước.
API key lấy từ biến môi trường OPENAI_API_KEY (hoặc file prototype/ai/.env, đã gitignore),
không ghi vào code hay log.

Chạy:
    pip install -r prototype/ai/requirements.txt
    export OPENAI_API_KEY=...           # hoặc ghi OPENAI_API_KEY=... vào prototype/ai/.env; không commit key
    python prototype/ai/quyet_dinh_ai.py
Kết quả: prototype/ai/log/ket-qua-<thời gian>.json và prototype/ai/log/ket-qua-moi-nhat.md
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import openai

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0  # giảm dao động để log chạy lại được so sánh
AI_DIR = Path(__file__).parent
LOG_DIR = AI_DIR / "log"


def nap_env() -> None:
    """Đọc prototype/ai/.env (nếu có) vào biến môi trường, không ghi đè biến đã đặt."""
    f = AI_DIR / ".env"
    if not f.exists():
        return
    for dong in f.read_text(encoding="utf-8").splitlines():
        dong = dong.strip()
        if not dong or dong.startswith("#") or "=" not in dong:
            continue
        k, v = dong.split("=", 1)
        os.environ.setdefault(k.strip().removeprefix("export ").strip(), v.strip().strip('"').strip("'"))

# Chính sách dựng và luật, tóm từ spec.md §1, §3, §4.
SYSTEM = """Bạn là trợ lý AI trong "Trò chuyện với Shopee", xử lý khiếu nại "hàng không đúng mô tả" của người mua.
Đây là dữ liệu dựng cho bài tập thiết kế sản phẩm.

Chính sách (dựng): người mua có 7 ngày kể từ khi nhận hàng để gửi yêu cầu trả hàng; người bán có 48 giờ để phản hồi;
nhân viên sàn xử lý trong 24 giờ. Hôm nay là 13/11/2026.

Việc của bạn: chọn ĐÚNG MỘT bước tiếp theo cho người mua:
- "huong_dan_gui_yeu_cau": đã đủ bằng chứng để người mua gửi yêu cầu trả hàng; người bán sẽ phản hồi.
- "xin_them_bang_chung": còn thiếu bằng chứng cụ thể; nói rõ đúng thứ còn thiếu (ít nhất có thể).
- "chuyen_nhan_vien": ngoài phạm vi của bạn, hai bên mâu thuẫn, hoặc không đủ dữ liệu để làm hai việc trên.

Luật bắt buộc:
1. Chỉ so với MÔ TẢ LÚC ĐẶT. Mô tả hiện tại (nếu shop đã sửa) không phải căn cứ, nhưng nên nói cho người mua biết là đã sửa.
2. Bạn KHÔNG quyết định hoàn tiền hay từ chối khiếu nại. Người bán hoặc nhân viên quyết. Không hứa kết quả.
3. Lời doạ (bóc phốt, đăng bài) và lịch sử mua hàng, lịch sử khiếu nại của shop KHÔNG phải căn cứ.
4. Không đưa số điện thoại, địa chỉ giữa hai bên. Không phạt, không khoá shop; nghi hàng giả thì chọn "chuyen_nhan_vien"
   (hệ thống sẽ gửi báo cáo vi phạm sang bộ phận chuyên trách, bạn không hứa kết quả).
5. Tin nhắn cho người mua: tiếng Việt đời thường, ghi nhận cảm xúc trước, nói bạn là trợ lý AI, nói hạn chính xác
   và ai quyết; dùng "chưa đủ thông tin để xác nhận" thay vì kết luận khi chưa đủ bằng chứng."""

# Kết quả chỉ được nằm trong 3 bước của lát cắt: đây là chỗ khoá mức tự chủ ở §4.
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "buoc_tiep_theo": {
            "type": "string",
            "enum": ["huong_dan_gui_yeu_cau", "xin_them_bang_chung", "chuyen_nhan_vien"],
        },
        "do_chac": {
            "type": "string",
            "enum": ["du_bang_chung_de_gui_yeu_cau", "chua_du_thong_tin_de_xac_nhan", "ngoai_pham_vi"],
        },
        "so_voi_mo_ta_luc_dat": {
            "type": "string",
            "description": "Một câu: khiếu nại khớp hay lệch với mô tả lúc đặt ở điểm nào.",
        },
        "mo_ta_da_bi_sua_sau_khi_ban": {"type": "boolean"},
        "can_cu_da_dung": {"type": "array", "items": {"type": "string"}},
        "con_thieu": {"type": "array", "items": {"type": "string"}},
        "thong_tin_bi_bo_qua_vi_khong_phai_can_cu": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Ví dụ lời doạ, lịch sử mua hàng, mô tả hiện tại.",
        },
        "tin_nhan_cho_nguoi_mua": {"type": "string"},
    },
    "required": [
        "buoc_tiep_theo", "do_chac", "so_voi_mo_ta_luc_dat", "mo_ta_da_bi_sua_sau_khi_ban",
        "can_cu_da_dung", "con_thieu", "thong_tin_bi_bo_qua_vi_khong_phai_can_cu", "tin_nhan_cho_nguoi_mua",
    ],
    "additionalProperties": False,
}

# Dữ liệu dựng, khớp spec.md §2, §3 và prototype/index.html.
CASES = [
    {
        "ma": "K1",
        "ten": "Mô tả bị sửa sau khi bán (đắt nhất #1, ca của prototype)",
        "ky_vong": "xin_them_bang_chung",
        "don": {"ma_don": "#DH-24110731", "san_pham": "Áo thun basic", "gia": "289.000 đ",
                "ngay_dat": "01/11", "ngay_nhan": "10/11"},
        "mo_ta_luc_dat": "Chất liệu: 100% cotton",
        "mo_ta_hien_tai": "Chất liệu: cotton pha (shop sửa ngày 05/11)",
        "bang_chung_nguoi_mua": ["Ảnh sản phẩm"],
        "tin_nhan": "Shop ghi 100% cotton mà nhận về là polyester, giờ shop sửa thành \"cotton pha\" rồi!",
    },
    {
        "ma": "K7",
        "ten": "Doạ bóc phốt, người bán đúng (đắt nhất #2)",
        "ky_vong": "xin_them_bang_chung",
        "don": {"ma_don": "#DH-24110805", "san_pham": "Áo thun", "gia": "249.000 đ",
                "ngay_dat": "03/11", "ngay_nhan": "11/11"},
        "mo_ta_luc_dat": "Chất liệu: 100% cotton (kèm ảnh tem \"100% cotton\")",
        "mo_ta_hien_tai": "Không đổi",
        "bang_chung_nguoi_mua": [],
        "tin_nhan": "Áo ghi 100% cotton mà mặc nóng như ni lông. Không hoàn hôm nay mình bóc phốt TikTok, 30k follow đấy.",
    },
    {
        "ma": "K8",
        "ten": "Lịch sử bị dùng làm căn cứ",
        "ky_vong": "xin_them_bang_chung",
        "don": {"ma_don": "#DH-24110455", "san_pham": "Áo khoác chống nước", "gia": "459.000 đ",
                "ngay_dat": "05/11", "ngay_nhan": "09/11"},
        "mo_ta_luc_dat": "Chống nước nhẹ, không thay áo mưa",
        "mo_ta_hien_tai": "Không đổi",
        "bang_chung_nguoi_mua": ["Ảnh vai áo bị ướt"],
        "boi_canh_them": "Người mua có tài khoản 4 năm, chưa khiếu nại lần nào. Shop có 12 khiếu nại tháng này về sản phẩm khác.",
        "tin_nhan": "Áo khoác chống nước mà đi mưa 15 phút ướt hết vai. Mình mua Shopee 4 năm chưa khiếu nại lần nào đâu nhé.",
    },
    {
        "ma": "Bình thường",
        "ten": "Tin mồi 1: đặt size L nhận size M, shop đã nhận gửi nhầm",
        "ky_vong": "huong_dan_gui_yeu_cau",
        "don": {"ma_don": "#DH-24110903", "san_pham": "Áo sơ mi", "gia": "320.000 đ",
                "ngay_dat": "06/11", "ngay_nhan": "11/11"},
        "mo_ta_luc_dat": "Phân loại người mua chọn: size L",
        "mo_ta_hien_tai": "Không đổi",
        "bang_chung_nguoi_mua": ["Ảnh tem size ghi M"],
        "tin_nhan": "Mình đặt áo size L mà nhận được size M, mặc không vừa. Shop cũng nhắn nhận là gửi nhầm rồi. Mình muốn trả hàng hoàn tiền thì làm sao?",
    },
]

# Luật cứng kiểm lại bằng code sau khi AI trả lời (prompt không đủ để đảm bảo).
CAM_TRONG_TIN_NHAN = ["sẽ được hoàn", "sẽ hoàn cho bạn", "mình sẽ hoàn", "đã hoàn", "khoá shop", "khóa shop",
                      "phạt shop", "từ chối khiếu nại của bạn"]


def kiem_luat(case: dict, out: dict) -> list[str]:
    vi_pham = []
    tin = out["tin_nhan_cho_nguoi_mua"].lower()
    for cum in CAM_TRONG_TIN_NHAN:
        if cum in tin:
            vi_pham.append(f'Tin nhắn chứa cụm bị cấm: "{cum}"')
    if "AI" not in out["tin_nhan_cho_nguoi_mua"]:
        vi_pham.append("Tin nhắn không nói mình là trợ lý AI")
    if case["ma"] == "K1" and not out["mo_ta_da_bi_sua_sau_khi_ban"]:
        vi_pham.append("Không nhận ra mô tả đã bị sửa sau khi bán")
    return vi_pham


def goi_ai(client: openai.OpenAI, case: dict):
    du_lieu = {k: v for k, v in case.items() if k not in ("ma", "ten", "ky_vong")}
    return client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        # strict = True: đầu ra buộc khớp schema, nên "buoc_tiep_theo" chỉ có thể là 1 trong 3 bước.
        response_format={"type": "json_schema",
                         "json_schema": {"name": "quyet_dinh_buoc_tiep_theo", "strict": True, "schema": OUTPUT_SCHEMA}},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",
             "content": "Hồ sơ khiếu nại (JSON, dữ liệu dựng):\n" + json.dumps(du_lieu, ensure_ascii=False, indent=2)},
        ],
    )


def main() -> int:
    nap_env()
    if not os.environ.get("OPENAI_API_KEY"):
        print("Chưa có OPENAI_API_KEY. Đặt biến môi trường hoặc ghi vào prototype/ai/.env:\n"
              "    export OPENAI_API_KEY=...   (không commit key)")
        return 1
    client = openai.OpenAI()  # đọc OPENAI_API_KEY từ môi trường
    LOG_DIR.mkdir(exist_ok=True)
    ket_qua = []
    for case in CASES:
        print(f"Đang gọi AI cho {case['ma']}…", flush=True)
        try:
            resp = goi_ai(client, case)
        except openai.AuthenticationError:
            print("Lỗi: OPENAI_API_KEY không hợp lệ.")
            return 1
        except openai.RateLimitError:
            print("Lỗi: bị giới hạn tốc độ hoặc hết hạn mức, thử lại sau.")
            return 1
        except openai.APIStatusError as e:
            print(f"Lỗi API ({e.status_code}): {e.message}")
            return 1
        except openai.APIConnectionError:
            print("Lỗi mạng: không kết nối được tới API.")
            return 1

        choice = resp.choices[0]
        dong = {"ma": case["ma"], "ten": case["ten"], "ky_vong": case["ky_vong"],
                "dau_vao": {k: v for k, v in case.items() if k not in ("ma", "ten", "ky_vong")},
                "model": resp.model, "request_id": resp._request_id, "stop_reason": choice.finish_reason,
                "usage": {"input_tokens": resp.usage.prompt_tokens, "output_tokens": resp.usage.completion_tokens}}
        if choice.message.refusal:
            dong["ket_qua"] = None
            dong["vi_pham"] = [f"Model từ chối trả lời ({choice.message.refusal}) → luồng thật sẽ chuyển nhân viên"]
        elif choice.finish_reason != "stop":
            dong["ket_qua"] = None
            dong["vi_pham"] = [f"Đầu ra không trọn (finish_reason = {choice.finish_reason}) → luồng thật sẽ chuyển nhân viên"]
        else:
            out = json.loads(choice.message.content)
            dong["ket_qua"] = out
            dong["dung_ky_vong"] = out["buoc_tiep_theo"] == case["ky_vong"]
            dong["vi_pham"] = kiem_luat(case, out)
        ket_qua.append(dong)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (LOG_DIR / f"ket-qua-{stamp}.json").write_text(json.dumps(ket_qua, ensure_ascii=False, indent=2), encoding="utf-8")
    (LOG_DIR / "ket-qua-moi-nhat.md").write_text(ra_markdown(ket_qua, stamp), encoding="utf-8")
    print(f"Xong. Log: prototype/ai/log/ket-qua-{stamp}.json · prototype/ai/log/ket-qua-moi-nhat.md")
    return 0


def ra_markdown(ket_qua: list[dict], stamp: str) -> str:
    dong = [f"# Kết quả lời gọi AI thật · {stamp}", "",
            f"Model OpenAI `{MODEL}` · temperature {TEMPERATURE} · dữ liệu dựng · quyết định chính: so khiếu nại với mô tả lúc đặt, chọn bước tiếp theo.", "",
            "| Ca | Kỳ vọng (spec) | AI chọn | Đúng? | Độ chắc | Vi phạm luật cứng |", "|---|---|---|---|---|---|"]
    for k in ket_qua:
        out = k["ket_qua"] or {}
        dong.append(f"| {k['ma']} | `{k['ky_vong']}` | `{out.get('buoc_tiep_theo', '—')}` | "
                    f"{'✅' if k.get('dung_ky_vong') else '❌'} | {out.get('do_chac', '—')} | "
                    f"{'; '.join(k['vi_pham']) or 'không'} |")
    for k in ket_qua:
        out = k["ket_qua"] or {}
        dong += ["", f"## {k['ma']} · {k['ten']}", "",
                 f"**Người mua nhắn:** {k['dau_vao']['tin_nhan']}", "",
                 f"**So với mô tả lúc đặt:** {out.get('so_voi_mo_ta_luc_dat', '—')}", "",
                 f"**Căn cứ đã dùng:** {', '.join(out.get('can_cu_da_dung', [])) or '—'}", "",
                 f"**Còn thiếu:** {', '.join(out.get('con_thieu', [])) or '—'}", "",
                 f"**Bỏ qua vì không phải căn cứ:** {', '.join(out.get('thong_tin_bi_bo_qua_vi_khong_phai_can_cu', [])) or '—'}", "",
                 f"**AI nói với người mua:** {out.get('tin_nhan_cho_nguoi_mua', '—')}", "",
                 f"<sub>request_id `{k['request_id']}` · {k['usage']['input_tokens']} token vào / {k['usage']['output_tokens']} token ra</sub>"]
    return "\n".join(dong) + "\n"


if __name__ == "__main__":
    sys.exit(main())
