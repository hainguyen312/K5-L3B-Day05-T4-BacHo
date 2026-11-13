# Prototype · T4 Thương mại điện tử · Nhóm BacHo

Ca dựng: **K1 — mô tả bị sửa sau khi bán**. Áo đặt 01/11 khi mô tả ghi "100% cotton", shop sửa thành "cotton pha" ngày 05/11, người mua nhận hàng 10/11, hạn trả hàng hết 17/11. Toàn bộ là **dữ liệu dựng** (đơn, shop, người mua).

Spec đầy đủ: [`../spec.md`](../spec.md) (§5 là phần prototype).

```
prototype/
├── index.html              # prototype bấm được (mock, không gọi AI)
├── screenshot-*.png        # ảnh đánh số cho §5
└── ai/
    ├── quyet_dinh_ai.py    # lời gọi AI thật (OpenAI gpt-4.1-mini) cho quyết định chính
    ├── requirements.txt
    └── log/                # kết quả mỗi lần chạy (tạo ra khi chạy script)
```

---

## 1. Prototype giao diện — `index.html`

Mở `index.html` bằng trình duyệt. Không cần cài, không backend, không gửi dữ liệu đi đâu. Câu AI là câu viết sẵn đúng nguyên văn spec §3.

Một trang có hai màn hình cho cùng một hồ sơ: **chat người mua** (trái) và **Kênh người bán** (phải). Thanh trên cùng đổi 3 mức tự chủ của `thuc_hien_hoan_tien`:

| Nút | Mức | Điều xảy ra |
|---|---|---|
| ① | Chỉ hướng dẫn — người mua tự làm | Người mua tự điền lại mọi thứ AI đã biết |
| ② | Cần người duyệt (người bán / nhân viên) — mức nhóm chọn | Yêu cầu trả hàng điền sẵn, người mua tự bấm gửi; người bán duyệt hoàn tiền |
| ③ | AI tự hoàn + hoàn tác | Để chỉ ra vì sao mức này bị loại |

### Bấm qua ca khó (mức ②)

1. Đọc 4 bong bóng AI, thẻ so sánh hai bản mô tả, checklist bằng chứng.
2. Bấm **"Gửi ảnh tem vải & gửi yêu cầu"** → Kênh người bán hiện yêu cầu, đếm ngược 48 giờ.
3. Ở Kênh người bán chọn một trong:
   - **"Đồng ý hoàn"** → hộp xác nhận có ô tick "không rút lại được".
   - **"Gửi bằng chứng phản hồi"** hoặc **"⏩ Giả lập: hết 48 giờ, không phản hồi"** → hồ sơ chuyển nhân viên sàn (24 giờ).

Đường phụ: **"AI hiểu sai? Báo lỗi"** (chọn "So nhầm bản mô tả" để thấy AI nhận lỗi và so lại) · **"Nói chuyện với người thật"** (thanh cố định đầu khung chat) / **"Gặp nhân viên"**. Nút **"⏩ Giả lập: người mua không làm gì, còn 24 giờ"** thay cho việc chờ thời gian thật.

Mở thẳng một trạng thái qua URL, ví dụ `index.html?l=2&s=sent` (mức ②, đã gửi yêu cầu).

**Chưa dựng:** màn hình nhân viên sàn, ca K7. Prototype dừng ở trạng thái "hồ sơ đã chuyển nhân viên".

### Ảnh

| File | Nội dung |
|---|---|
| `screenshot-muc2.png` | Người mua, mức ②, trước khi gửi |
| `screenshot-nguoi-ban.png` | Sau khi gửi, Kênh người bán đếm 48 giờ |
| `screenshot-nguoi-ban-gui-bang-chung.png` | Người bán gửi bằng chứng → chuyển nhân viên |
| `screenshot-nguoi-ban-dong-y-hoan-tien.png` | Người bán đồng ý hoàn tiền (hộp xác nhận) |

---

## 2. Lời gọi AI thật — `ai/quyet_dinh_ai.py`

**Model:** OpenAI **`gpt-4.1-mini`**, `temperature = 0`, Chat Completions với Structured Outputs (`json_schema`, `strict: true`).

**Quyết định AI làm:** đọc khiếu nại "không đúng mô tả", so với **mô tả lúc đặt** (không phải mô tả hiện tại), rồi chọn **đúng một** bước tiếp theo:

| Bước | Khi nào |
|---|---|
| `huong_dan_gui_yeu_cau` | Đủ bằng chứng để người mua gửi yêu cầu trả hàng |
| `xin_them_bang_chung` | Còn thiếu bằng chứng, nói rõ thiếu gì |
| `chuyen_nhan_vien` | Ngoài phạm vi, hai bên mâu thuẫn, hoặc nghi hàng giả |

**Mức tự chủ (spec §4) được khoá bằng code, không chỉ bằng prompt:**
- Schema đầu ra (strict) chỉ có 3 bước trên → AI **không thể** trả về "hoàn tiền", "từ chối" hay "phạt shop".
- Sau khi AI trả lời, code kiểm thêm luật cứng: không hứa kết quả, không nhắc khoá/phạt shop, phải nói mình là trợ lý AI, K1 phải nhận ra mô tả đã bị sửa. Vi phạm được ghi vào log.
- Model từ chối (`refusal`) hoặc đầu ra không trọn → ghi log, luồng thật sẽ chuyển nhân viên.

**Ca chạy** (khớp spec §2, §3): K1 mô tả bị sửa sau khi bán · K7 doạ bóc phốt, người bán đúng · K8 lịch sử bị dùng làm căn cứ · ca bình thường (đặt L nhận M, shop đã nhận gửi nhầm). Mỗi ca có cột **kỳ vọng theo spec** để so với lựa chọn của AI.

### Chạy

Từ thư mục gốc repo:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r prototype/ai/requirements.txt

export OPENAI_API_KEY=sk-...        # hoặc ghi OPENAI_API_KEY=sk-... vào prototype/ai/.env
python prototype/ai/quyet_dinh_ai.py
```

API key chỉ để ở biến môi trường hoặc `prototype/ai/.env` (đã có trong `.gitignore`). **Không commit key**, key không được ghi vào log.

### Log

Mỗi lần chạy tạo:

| File | Nội dung |
|---|---|
| `ai/log/ket-qua-<YYYYMMDD-HHMMSS>.json` | Đầy đủ: đầu vào, kết quả JSON của AI, `model`, `request_id`, `finish_reason`, số token, đúng/sai kỳ vọng, vi phạm luật cứng |
| `ai/log/ket-qua-moi-nhat.md` | Bảng tóm tắt (ca · kỳ vọng · AI chọn · đúng? · độ chắc · vi phạm) + chi tiết từng ca, kể cả câu AI nói với người mua |

Đọc nhanh: mở `ai/log/ket-qua-moi-nhat.md`.

### Giới hạn

- Chỉ dữ liệu dựng; không đưa dữ liệu người dùng thật vào công cụ AI.
- Script chạy riêng, **chưa nối** vào `index.html`: prototype giao diện vẫn dùng câu viết sẵn.
- Kiểm luật cứng bằng so khớp cụm từ, chỉ bắt được các cách nói đã liệt kê.
