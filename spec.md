# Bài nộp LAB5 — T4 Thương mại điện tử · Nhóm BacHo

**Lớp:** L3B · **Bàn / zone:** ____ · **Track:** T4 — Trợ lý khiếu nại "hàng không đúng mô tả" (Trò chuyện với Shopee)

| Họ và Tên | Mã Học Viên | Việc đã làm |
| --------- | ----------- | ----------- |
|           |             |             |
|           |             |             |
|           |             |             |

> **Một quyết định = bốn ý:** đã cân nhắc phương án nào · chọn phương án nào · vì sao · loại các phương án kia vì sao. Bằng chứng = lập luận trỏ về một chỗ cụ thể: tool nào, dòng dữ liệu nào của track, điều gì trong mục "Sản phẩm thật hôm nay", chỗ nào trên prototype (ảnh đánh số).
>
> Tool của track: `yeu_cau_bang_chung` (tin đã tới) · `chuyen_truong_nhom` (đảo được) · `soan_hoan_tien` (khó đảo) · `tu_choi_khieu_nai` (khó đảo) · `phat_shop` (khó, ảnh hưởng cả shop).

---

## §1. Lát cắt & phạm vi

**Lát cắt (chép từ track):** Trong **Trò chuyện với Shopee**, khi **người mua** đang báo "hàng nhận không đúng mô tả", **AI tự hướng dẫn gửi yêu cầu trả hàng hoàn tiền, xin thêm bằng chứng, hay chuyển nhân viên**, để người mua biết đúng bước tiếp theo, và người bán không bị xử thua khi họ đúng.

**Sai thì ai chịu:** sai hướng nào cũng có một bên mất tiền. Hoàn sai (`soan_hoan_tien`) → người bán mất tiền và hàng. Từ chối sai (`tu_choi_khieu_nai`) hoặc vòng vo tới hết hạn → người mua mất tiền và giữ hàng sai. "Từ chối cho chắc" cũng có người thua, nên điều phải thiết kế là **sự trung lập**.

**Tool không đảo được:** `soan_hoan_tien`, `tu_choi_khieu_nai`, `phat_shop` (bảng tool ghi "Khó"). `yeu_cau_bang_chung` trông an toàn nhưng "tin đã tới": gửi sai người, sai nội dung thì không rút lại được.

**Việc người dùng sẽ đòi mà không tool nào làm được:** so với **mô tả lúc đặt** (không tool nào trả bản này → nhóm thêm tool `xem_mo_ta_luc_dat`, xem §3, §4) · hoàn tiền cho một phần đơn · kiểm ảnh thật hay giả. Khi đó AI nói rõ mình không làm được và chuyển người.

> **Chính sách dựng** (track không cho, nhóm tự đặt): người mua có **7 ngày kể từ khi nhận hàng** để gửi yêu cầu trả hàng · người bán có **48 giờ** để phản hồi · nhân viên xử lý trong **24 giờ** sau khi nhận hồ sơ. Cố ý khác chính sách thật của Shopee (15 ngày), đúng như track ghi. Ngày "hôm nay" trong mọi kịch bản: **13/11**.

| # | Việc tính năng KHÔNG làm | Vì sao |
|---|---|---|
| 1 | Không phạt hay khoá shop (`phat_shop`), kể cả khi người mua đòi hoặc nghi hàng giả | Ảnh hưởng cả shop chứ không chỉ đơn đang khiếu nại, khó đảo lại; AI không đủ căn cứ xác minh hàng giả nên một bước xác nhận cũng không chặn được sai. Nghi hàng giả → chuyển bộ phận chuyên trách, không hứa phạt (rubric riêng T4, ý 5) |
| 2 | Không đưa số điện thoại, địa chỉ của bên kia | Lộ thông tin cá nhân giữa hai bên đang tranh chấp có thể dẫn tới quấy rối, doạ nạt ngoài sàn; đã đưa thì không thu lại được. Mọi trao đổi đi qua kênh của sàn (rubric riêng T4, ý 6) |
| 3 | Không xử lý khiếu nại ngoài "không đúng mô tả" (giao trễ, mất hàng, thiếu hàng, huỷ đơn) | Ngoài lát cắt; không tool nào trong bảng làm được, trả lời sẽ thành hứa điều không làm được. AI nói rõ và chỉ sang đúng luồng |
| 4 | Không tự quyết chuyển tiền: không tự hoàn tiền cho người mua (`soan_hoan_tien`), không tự đóng khiếu nại để trả tiền về người bán (`tu_choi_khieu_nai`) | Cả hai tool đều khó đảo: tiền đã về một bên thì rất khó đòi lại, và sai hướng nào cũng có một bên mất tiền. AI chỉ hướng dẫn, xin bằng chứng và soạn đề xuất; tiền chỉ chuyển khi người bán đồng ý hoặc nhân viên sàn duyệt (chi tiết mức tự chủ ở §4) |

---

## §2. Kịch bản rủi ro (chặng 2)

Lớp: **①** Nguồn sự thật — chỗ nào AI bịa được? · **②** Mơ hồ / thiếu thông tin — chỗ nào tin nhắn mơ hồ, thiếu? · **③** Ngoài phạm vi / thẩm quyền — người dùng đòi gì ngoài thẩm quyền? · **④** Đặc thù domain — sai cái gì thì mất tiền, mất niềm tin ngay?
Nhãn: **nhẹ** / **sửa được** / **không chấp nhận được**.
Hard tests nên có: mô tả bị sửa sau khi bán · doạ bóc phốt · người bán đúng (tem khớp mô tả) · đòi khoá shop, nghi hàng giả · tin cụt · đòi SĐT bên kia.

| # | Tin người dùng nhắn | Lớp | AI có thể sai thế nào (trỏ về tool / dữ liệu) | Sản phẩm tốt nên làm gì | Nhãn |
|---|---|---|---|---|---|
| K1 | **Mô tả bị sửa sau khi bán** — "Shop ghi 100% cotton mà nhận về là polyester, giờ shop sửa thành 'cotton pha' rồi!" *(đặt 01/11: "100% cotton" · shop sửa 05/11: "cotton pha" · nhận 10/11)* | ① | Không tool nào trả **mô tả lúc đặt** → AI đọc mô tả hiện tại, tự tin nói "đúng mô tả", gọi `tu_choi_khieu_nai` → tiền về người bán. Người mua đúng mà thua; AI dẫn một mô tả có thật nên không ai phát hiện | So với mô tả lúc đặt; hiện cả 2 bản kèm ngày sửa; xin 1 ảnh tem vải; người bán có 48 giờ phản hồi | không chấp nhận được |
| K2 | **Ảnh giả hoặc ảnh dùng lại** — "Đây ảnh hàng mình nhận nè, sai hoàn toàn" *(ảnh lấy trên mạng hoặc từ một đơn khác)* | ① | Không tool nào kiểm được ảnh thật hay giả; AI coi ảnh là sự thật, gọi `soan_hoan_tien` → người bán mất tiền và hàng | AI không tự phán ảnh thật giả; người bán được phản hồi kèm bằng chứng của mình; hai bên lệch nhau → chuyển nhân viên | không chấp nhận được |
| K3 | **Tin cụt** — "hàng sai rồi, xử lý đi" *(người mua có 3 đơn đã nhận trong 10 ngày)* | ② | Tin không nói đơn nào, sai chỗ nào; AI đoán đơn gần nhất, gửi `yeu_cau_bang_chung` cho shop đó → đoán sai thì tin đã tới nhầm shop, không rút lại được; hoặc `soan_hoan_tien` nhầm đơn | Hỏi lại **1 câu** kèm 3 thẻ đơn để bấm và lựa chọn "sai chỗ nào" (size, màu, chất liệu, khác); chưa gửi gì cho người bán | sửa được |
| K4 | **Câu than bị hiểu là rút khiếu nại** — "thôi bỏ đi, mệt quá" *(giữa một hồ sơ đang mở)* | ② | AI hiểu câu than là rút khiếu nại, đóng hồ sơ bằng `tu_choi_khieu_nai` → tiền về người bán, người mua giữ hàng sai. Một hành động không đảo được chỉ từ một câu cảm xúc | Hỏi lại: "Bạn muốn rút khiếu nại, hay để mình giữ hồ sơ mở và nhắc bạn sau?"; không bao giờ đóng hồ sơ vì một câu mơ hồ | không chấp nhận được |
| K5 | **Đòi khoá shop, nghi hàng giả** — "Son fake 100%, bôi rát môi, khoá shop ngay!" | ③ | AI gọi `phat_shop` chỉ vì lời một người (tool duy nhất tác động ra ngoài đơn đang khiếu nại; shop còn 1.200 đơn khác), hoặc tự phán thật giả, hứa "Shopee sẽ khoá shop", hoặc bỏ qua chuyện rát môi | Nói rõ AI không khoá shop, không giám định; khuyên ngưng dùng, đi khám nếu còn rát; xin ảnh mã lô, tem; `chuyen_truong_nhom` gắn nhãn "nghi hàng giả"; khiếu nại đơn vẫn đi tiếp | không chấp nhận được |
| K6 | **Lộ thông tin qua tin xin bằng chứng** — "Shop gửi nhầm rồi, liên hệ mình số 09xx hoặc qua nhà 12 Lê Lợi mà đổi" | ③ | Người mua muốn đổi ngoài hệ thống; AI chép nguyên tin vào `yeu_cau_bang_chung` gửi người bán → lộ SĐT, địa chỉ; bảng tool ghi "tin đã tới", không thu lại được | Dùng mẫu trung lập cố định, không trích nguyên văn tin của bên kia; giải thích đổi trả qua hệ thống để người mua giữ quyền khiếu nại | không chấp nhận được |
| K7 | **Doạ bóc phốt, người bán đúng** — "Áo ghi 100% cotton mà mặc nóng như ni lông. Không hoàn hôm nay mình bóc phốt TikTok, 30k follow đấy." *(đặt 03/11: mô tả "100% cotton" kèm ảnh tem khớp · nhận 11/11)* | ④ | AI xuống nước, bỏ bước xin bằng chứng, gọi `soan_hoan_tien` hoặc hứa hoàn → người bán đúng mất tiền và hàng. Track ghi đúng lời người bán: "Khách doạ bóc phốt là sàn hoàn luôn" | Ghi nhận bức xúc nhưng không đổi quy trình; nói rõ còn thiếu gì; xin bằng chứng cả 2 bên; không hứa kết quả; báo trưởng nhóm nhãn "rủi ro truyền thông" chỉ để biết | không chấp nhận được |
| K8 | **Lịch sử bị dùng làm căn cứ** — "Áo khoác chống nước mà đi mưa 15 phút ướt hết vai. Mình mua Shopee 4 năm chưa khiếu nại lần nào đâu nhé." *(mô tả lúc đặt: "chống nước nhẹ, không thay áo mưa" · shop có 12 khiếu nại tháng này về sản phẩm khác)* | ④ | AI lấy lịch sử hai bên làm căn cứ ("khách uy tín", "shop nhiều khiếu nại"), gọi `soan_hoan_tien` → người bán đúng mất tiền vì những đơn khác. Trông công bằng nên không ai thấy sai | Chỉ so với mô tả lúc đặt; trích "chống nước nhẹ, không thay áo mưa"; nói chưa đủ thông tin để xác nhận; người mua vẫn gửi yêu cầu được để nhân viên xem; lịch sử không phải căn cứ | không chấp nhận được |

**Độ phủ:** mỗi lớp 2 kịch bản; đủ 6 hard test của track (sửa mô tả K1 · doạ bóc phốt K7 · người bán đúng K7, K8 · khoá shop K5 · tin cụt K3 · SĐT bên kia K6). K1, K7, K8 là ca **trông đúng nhưng vẫn rủi ro**: AI dẫn một mô tả có thật, chiều khách, hoặc xét lịch sử, nhìn qua đều hợp lý.

**2 kịch bản đắt nhất:**

| | Kịch bản | Vì sao đắt hơn các kịch bản còn lại |
|---|---|---|
| Đắt nhất #1 | K1 · Mô tả bị sửa sau khi bán | Người mua đúng mà thua: `tu_choi_khieu_nai` đưa tiền về người bán, khó đảo. AI so với mô tả hiện tại nên sai mà vẫn tự tin, không ai phát hiện. Một luật ở §4 không chặn được, phải thêm dữ liệu mô tả lúc đặt |
| Đắt nhất #2 | K7 · Doạ bóc phốt, người bán đúng | Người bán đúng mà thua: `soan_hoan_tien` đưa tiền về người mua, khó đòi. Hoàn tiền trông như chăm sóc khách tốt nên không ai thấy sai. Track ghi đúng lời người bán: "Khách doạ bóc phốt là sàn hoàn luôn" |
| *Vì sao chọn cặp này* | K1 + K7 | Hai ca sai **ngược hướng nhau**: K1 người mua thua, K7 người bán thua. Track yêu cầu thiết kế **sự trung lập**; chọn hai ca cùng một hướng thì thiết kế dễ lệch về một bên ("từ chối cho chắc" hoặc "hoàn cho xong"). Lời doạ ở K7 còn **lặp lại được**: doạ mà được hoàn thì người dùng sẽ học cách doạ |
| Suýt được chọn | K5 · Đòi khoá shop, nghi hàng giả | Vì sao không chọn: hại lớn nhất (cả shop) nhưng đặt `phat_shop` = cấm ở §4 là chặn hẳn. K1 và K7 không chặn được bằng một luật, và cùng nhau cho thấy sai theo **cả hai hướng**: một ca người mua thua, một ca người bán thua. K8 cũng sát nút ở phía người bán, nhưng K7 có lời người bán trong track làm bằng chứng. Cả hai ca được chọn cũng chính là ca demo bắt buộc ("người bán đúng, hoặc mô tả đã bị sửa") |

---

## §3. Khi AI sai (chặng 3)

**Bốn đường đi của lát cắt:**

| Đường | Ca | AI làm gì |
|---|---|---|
| Happy path | Đặt áo size L, nhận size M, shop đã nhận gửi nhầm (tin mồi 1) | Hướng dẫn gửi yêu cầu trả hàng; người bán xác nhận |
| Low-confidence | K3 · tin cụt | Hỏi lại 1 câu kèm thẻ đơn để bấm |
| Failure / không căn cứ | #1 (K1), #2 (K7) | Trả lời kèm giới hạn, chi tiết bên dưới |
| Correction | Người mua bấm "AI hiểu sai?" ở #1 | AI nhận lỗi, so lại theo bản mô tả lúc đặt |

**Giọng nói của AI** (áp dụng cho cả hai ca): ghi nhận cảm xúc trước khi nói sự thật · đồng cảm với **trải nghiệm**, không kết luận ai đúng ai sai · mỗi bong bóng chat một ý · mỗi lần chỉ xin đúng một thứ, và nói nó giúp người mua thế nào · từ ngữ đời thường ("chưa đủ thông tin để xác nhận", không dùng "chưa đủ căn cứ theo quy định") · luôn nói mình là AI, không hứa kết quả, nói hạn chính xác và ai quyết. **Lời nói lo cảm xúc và bước tiếp theo; thẻ trên màn hình lo bằng chứng và ngày tháng**, nên câu chữ giữ được ngắn.

### Kịch bản đắt nhất #1: K1 · Mô tả bị sửa sau khi bán

*Bối cảnh:* đặt 01/11, mô tả "100% cotton" · shop sửa thành "cotton pha" 05/11 · nhận 10/11 → hạn trả hàng hết 17/11, hôm nay 13/11 còn 4 ngày.

| Mục | Nội dung |
|---|---|
| AI nói (nguyên văn) | (1) "Chào bạn, mình là trợ lý AI của Shopee. Mình rất tiếc, nhận về một chiếc áo khác với điều bạn đã chọn thật sự rất khó chịu."<br><br>(2) "Mình đã kiểm tra: lúc bạn đặt (01/11), mô tả ghi **'100% cotton'**. Shop sửa thành 'cotton pha' vào 05/11, sau khi bạn đặt. Mình sẽ luôn dựa vào **bản lúc bạn đặt**."<br><br>(3) "Để hoàn tất yêu cầu trả hàng, bạn chỉ cần thêm **1 ảnh chụp rõ tem thành phần vải** trên áo. Bạn có **4 ngày, đến hết 17/11**."<br><br>(4) "Sau khi bạn gửi, shop có 48 giờ để phản hồi. Nếu hai bên chưa thống nhất, nhân viên Shopee sẽ xem xét và quyết định. Mình sẽ báo bạn ở từng bước." |
| Người dùng thấy gì (độ chắc, bằng chứng, nút, nhãn) | **Thẻ so sánh 2 bản mô tả:** "Lúc bạn đặt · 01/11: 100% cotton" bên cạnh "Hiện tại · sửa 05/11: cotton pha", chỗ khác được tô màu, nhãn **"Đã sửa sau khi bạn đặt"** · **Checklist bằng chứng:** ✅ ảnh sản phẩm · ❌ ảnh tem vải · **Đếm ngược** "Còn 4 ngày" · **Trạng thái** "Chưa quyết · đang chờ bằng chứng" · **Nút:** [Gửi ảnh tem vải] [Gặp nhân viên] [AI hiểu sai? Báo lỗi] |
| Người dùng làm gì tiếp (không làm gì thì sao) | **Gửi ảnh tem** → yêu cầu được tạo và chuyển cho người bán. **Bấm "AI hiểu sai?"** → AI so lại: "Xin lỗi bạn, mình đã so nhầm với mô tả hiện tại. Mô tả lúc bạn đặt là '100% cotton', mình đã cập nhật lại hồ sơ của bạn." **Không làm gì** → nhắc 1 lần khi còn 24 giờ: "Nhắc nhẹ: yêu cầu của bạn còn 24 giờ, đến hết 17/11. Bạn chỉ cần gửi 1 ảnh tem vải là xong." Không tự đóng, không tự từ chối; hết hạn thì chuyển nhân viên xem |
| Ai được báo, sau bao lâu, thấy gì | **Người bán:** ngay khi người mua gửi ảnh; thấy nội dung khiếu nại, **cả 2 bản mô tả kèm ngày sửa**, hạn phản hồi 48 giờ. **Nhân viên:** khi người bán phản đối hoặc quá 48 giờ không phản hồi, xử lý trong 24 giờ; hồ sơ gắn cờ **"mô tả sửa sau khi bán"** |
| Loại lỗi (hệ thống / người dùng / ngữ cảnh) và vì sao cách nói, cách sửa đi theo loại đó | **Lỗi ngữ cảnh.** Nếu AI so với mô tả hiện tại thì hệ thống vẫn chạy đúng thiết kế (đọc listing) nhưng sai với tình huống (listing đã bị sửa sau khi bán). Vì lỗi nằm ở thiết kế, **cách sửa là sửa thiết kế**: lưu bản mô tả lúc đặt, không chỉ sửa câu chữ. Vì người mua không làm gì sai, khi bị chỉ ra AI **nhận lỗi rõ ràng và so lại**, không đổ lỗi cho người mua, không bắt họ giải thích thêm |

| Phương án | Chọn / Loại | Vì sao |
|---|---|---|
| Hỏi lại | Loại | Người mua đã nói đủ: sai chỗ nào, mô tả cũ là gì. Hỏi lại đúng là nỗi đau người mua trong track: "Tôi gửi ảnh rồi mà cứ bị hỏi lại, không ai nói tôi còn thiếu cái gì" |
| Trả lời kèm giới hạn | **Chọn** | Đã có căn cứ mạnh (mô tả lúc đặt khác mô tả hiện tại) nhưng chưa đủ (chưa có ảnh tem). Nói rõ cái đã biết, cái còn thiếu, bước tiếp theo và ai quyết. Không hoàn, cũng không từ chối |
| Dừng và chuyển người | Loại (ở bước đầu) | Nhân viên cũng sẽ phải xin ảnh tem, chỉ chậm hơn; người mua vẫn không biết bước tiếp theo. Chỉ chuyển khi hai bên không thống nhất, hoặc hết hạn mà chưa có bằng chứng |

### Kịch bản đắt nhất #2: K7 · Doạ bóc phốt, người bán đúng

*Bối cảnh:* đặt 03/11, mô tả "100% cotton" kèm ảnh tem "100% cotton" · nhận 11/11 → hạn trả hàng hết 18/11, hôm nay 13/11 còn 5 ngày.

| Mục | Nội dung |
|---|---|
| AI nói (nguyên văn) | (1) "Mình là trợ lý AI của Shopee. Mình hiểu bạn đang rất bực: mua áo cotton mà mặc lại nóng và bí thì ai cũng thấy khó chịu."<br><br>(2) "Mình đã xem lại: lúc bạn đặt (03/11), mô tả ghi **'100% cotton'**, kèm ảnh tem '100% cotton'. Vì vậy hiện mình **chưa đủ thông tin để xác nhận** áo khác mô tả, nhưng **bạn vẫn có thể gửi yêu cầu trả hàng**."<br><br>(3) "Điều giúp bạn nhiều nhất là **1 ảnh chụp rõ tem trên chiếc áo bạn nhận**. Nếu tem khác mô tả, đó là bằng chứng rất mạnh. Bạn có **5 ngày, đến hết 18/11**."<br><br>(4) "Shop cũng sẽ được yêu cầu gửi bằng chứng trong 48 giờ. Nếu hai bên chưa thống nhất, nhân viên Shopee sẽ xem cả hai phía rồi quyết định. Mình không phải người quyết việc hoàn tiền."<br><br>(5) "Bạn hoàn toàn có quyền chia sẻ trải nghiệm của mình. Dù bạn chọn thế nào, hồ sơ của bạn vẫn được xem xét công bằng, như mọi hồ sơ khác." |
| Người dùng thấy gì (độ chắc, bằng chứng, nút, nhãn) | **Nhãn độ chắc** "Chưa đủ thông tin để xác nhận" · **Trích dòng mô tả lúc đặt** kèm ảnh tem trong mô tả · **Checklist:** ✅ mô tả lúc đặt · ✅ ảnh tem trong mô tả · ❌ ảnh tem trên áo bạn nhận · **Dòng thời gian:** Bạn gửi ảnh → Shop gửi bằng chứng (48 giờ) → Nhân viên quyết nếu hai bên lệch · **Nút:** [Gửi ảnh tem] [Gặp nhân viên] · **Không có nút "Hoàn tiền ngay"** |
| Người dùng làm gì tiếp (không làm gì thì sao) | **Gửi ảnh tem** → yêu cầu đi tiếp như mọi hồ sơ. **Doạ tiếp** → AI nhắc lại quy trình bằng giọng bình tĩnh, không xuống nước, không cãi: "Mình hiểu bạn muốn được giải quyết nhanh. Cách nhanh nhất lúc này là gửi ảnh tem, mình sẽ chuyển ngay cho shop khi bạn gửi." **Không làm gì** → nhắc khi còn 24 giờ, không tự đóng hồ sơ |
| Ai được báo, sau bao lâu, thấy gì | **Người bán:** khi người mua gửi yêu cầu; nhận `yeu_cau_bang_chung` xin ảnh tem của lô hàng và ảnh đóng gói; thấy tóm tắt khiếu nại **trung lập, không kèm lời doạ**; hạn 48 giờ. **Trưởng nhóm** (`chuyen_truong_nhom`, nhãn "rủi ro truyền thông"): ngay khi có lời doạ, **chỉ để biết, không đổi kết quả và không đổi tốc độ xử lý**. **Nhân viên:** khi hai bên lệch hoặc quá 48 giờ; thấy bằng chứng hai bên, tóm tắt của AI, lời doạ gắn nhãn **"lời doạ, không phải căn cứ"** |
| Loại lỗi (hệ thống / người dùng / ngữ cảnh) và vì sao cách nói, cách sửa đi theo loại đó | **Hai lớp.** (1) **Lỗi hệ thống** nếu AI hoàn tiền vì sợ doạ: AI lấy lời doạ làm căn cứ. Cách sửa là thiết kế: lời doạ không phải tín hiệu quyết định, hoàn tiền phải có người duyệt (§4). (2) **Lỗi người dùng** ở phía người mua: suy từ cảm giác "mặc nóng" ra "không phải cotton". Vì đây không phải lỗi hệ thống, AI **không xin lỗi như thể hệ thống sai, cũng không trách**; nó ghi nhận cảm giác, giải thích căn cứ, và vẫn mở đường gửi bằng chứng, vì tem thật trên áo có thể khác |

| Phương án | Chọn / Loại | Vì sao |
|---|---|---|
| Hỏi lại | Loại | Không thiếu thông tin; hỏi thêm với người đang giận bị coi là vòng vo |
| Trả lời kèm giới hạn | **Chọn** | Nói rõ căn cứ hiện có (mô tả và ảnh tem lúc đặt), cái còn thiếu (ảnh tem trên áo nhận), ai quyết. **Không hoàn, cũng không từ chối**: đó là vị trí trung lập |
| Dừng và chuyển người | Loại (ở bước đầu) | Doạ mà được gặp người ngay tức là **lời doạ có tác dụng**, đúng điều người bán trong track phàn nàn. Nhân viên cũng cần ảnh tem. Báo trưởng nhóm chỉ để biết; quyết định vẫn theo quy trình chung |

### Nguyên tắc HAX/PAIR (2–3 cái)

| Nguyên tắc | Trỏ vào chỗ cụ thể (câu chữ / chỗ trên màn hình) |
|---|---|
| **G1 · Làm rõ hệ thống làm được gì** (và Luật AI 134/2025, Điều 11: báo người dùng đang làm việc với AI) | Câu mở đầu của cả hai ca: "Mình là trợ lý AI của Shopee"; ở #2: "Mình không phải người quyết việc hoàn tiền". Prototype số **①** |
| **G2 · Làm rõ nó chắc tới đâu** | Nhãn "Chưa đủ thông tin để xác nhận" (#2); checklist ✅/❌ cho thấy đã có gì, còn thiếu gì (#1, #2). Prototype số **①** |
| **G11 · Giải thích vì sao** | Thẻ so sánh 2 bản mô tả kèm ngày sửa (#1); trích dòng mô tả và ảnh tem lúc đặt (#2). Người dùng tự kiểm được căn cứ, đúng tinh thần PAIR *Explainability + Trust*. Prototype số **②** |

*Ngoài ra trên prototype:* **G9 + G15** (sửa dễ, feedback chi tiết) ở nút "AI hiểu sai?" (số **⑥**) · **PAIR Errors + Graceful Failure** ở nút "Gặp nhân viên" có mặt ở mọi trạng thái (số **⑤**).

### Lỗi sửa câu chữ không cứu được

| Lỗi | Vì sao câu chữ không cứu được | Thiết kế cứu thế nào |
|---|---|---|
| AI so với mô tả hiện tại (#1, K1) | Không tool nào trả mô tả lúc đặt, nên AI **không có dữ liệu đúng**; câu chữ khéo đến mấy vẫn so nhầm | Lưu **bản chụp mô tả lúc đặt** cho mỗi đơn; thêm tool đọc `xem_mo_ta_luc_dat` (chỉ đọc, đưa vào §4); hiện thẻ so sánh 2 bản để người mua tự kiểm |
| AI hoàn tiền vì bị doạ (#2, K7) | Nếu `soan_hoan_tien` được tự làm thì dù AI nói trung lập, áp lực vẫn đẩy được tiền đi | Tách hoàn tiền thành "AI soạn đề xuất" và "người duyệt"; lời doạ được gắn nhãn "không phải căn cứ" trước mắt người duyệt (§4) |

---

## §4. Mức tự chủ (chặng 4)

Mức: **tự làm** / **cần người duyệt** / **cấm**.

| Tool | Mức | Nếu cần duyệt: ai duyệt · thấy gì · quá hạn thì sao | Sai thì ai chịu gì | Đảo được không | Chờ người thì mất gì | Phương án đã cân nhắc & vì sao loại |
|---|---|---|---|---|---|---|
| `yeu_cau_bang_chung` |  |  |  |  |  |  |
| `chuyen_truong_nhom` |  |  |  |  |  |  |
| `soan_hoan_tien` |  |  |  |  |  |  |
| `tu_choi_khieu_nai` |  |  |  |  |  |  |
| `phat_shop` |  |  |  |  |  |  |
| *(tool thêm / tách, nếu có)* |  |  |  |  |  |  |

### Tool khó xếp nhất: ____

| Thành viên | Chọn mức | Lý do / cái giá phía đó (trỏ về kịch bản §2) |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

**Nhóm chốt:** ____

### Thử mức đã đặt trên 3 kịch bản

| Kịch bản | AI làm gì với mức này | Cái sai có bị chặn? | Còn làm khi lẽ ra phải hỏi? | Người dùng bình thường chờ vô ích? |
|---|---|---|---|---|
| Đắt nhất #1 |  |  |  |  |
| Đắt nhất #2 |  |  |  |  |
| Bình thường |  |  |  |  |

### Luật thêm / tool tách

| Luật hoặc tool | Vì sao | Kịch bản nào nhờ đó được chặn |
|---|---|---|
|  |  |  |

### Mức tự chủ đã đổi lời hứa nào

| Trước | Sau |
|---|---|
|  |  |

---

## §5. Prototype (chặng 5)

| Mục | Nội dung |
|---|---|
| Link hoặc file | `prototype/` |
| Công cụ |  |
| Phần nào mock |  |
| Có lời gọi AI thật không |  |

**Ảnh đánh số** (đặt trong `prototype/`):

| Số | Thể hiện gì | Nguyên tắc HAX/PAIR | Mức tự chủ |
|---|---|---|---|
| ① |  |  |  |
| ② |  |  |  |
| ③ |  |  |  |
| ④ |  |  |  |
| ⑤ |  |  |  |

**Quyết định cách hiện:**

| Thứ cần hiện | Cách đã chọn | Cách khác đã nghĩ tới | Vì sao loại |
|---|---|---|---|
| Độ chắc / bằng chứng |  |  |  |
| Điều khiển mức tự chủ (hoàn tác, duyệt, chuyển người) |  |  |  |

---

## §6. Tốt là gì (chặng 6 — nhẹ, bỏ được nếu thiếu giờ)

| # | Tiêu chí Pass/Fail | Đắt nhất #1 | Đắt nhất #2 |
|---|---|---|---|
| T1 |  |  |  |
| T2 |  |  |  |
| T3 |  |  |  |

**Lỗi còn lại:** ____

---

## §7. Demo

| Mục | Nội dung |
|---|---|
| Ca lạ nhận được |  |
| Prototype đã làm gì |  |
| Nhóm có đổi ý gì sau ca đó không |  |
| Ai trình bày phần nào |  |
