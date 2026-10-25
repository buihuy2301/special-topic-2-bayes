# Rà soát văn phong ba báo cáo

Ngày rà soát: 25/10/2026. Phạm vi: đọc nguồn LaTeX hiện có của bài thường xuyên, giữa kỳ và cuối kỳ; đối chiếu cách dùng từ và diễn giải giữa ba bài. Đây là rà soát biên tập; các góp ý đã được áp dụng vào nguồn LaTeX ngày 25/10/2026. Không chạy lại phân tích thống kê. Kết quả biên dịch được ghi ở cuối tài liệu. Các số dòng dưới đây tính theo nguồn tại thời điểm rà soát.

## Nhận xét chung

Cả ba bài đã có văn phong khá rõ, câu tương đối ngắn và bố cục bám đề. Bài thường xuyên giữ được giọng cá nhân qua bài toán vận hành dữ liệu; bài giữa kỳ nối công thức với mô phỏng; bài cuối kỳ nêu rõ điều kiện của phần lớn kết quả. Không cần viết lại toàn bộ hoặc tăng mức trang trọng bằng những từ khó hơn.

Những việc nên ưu tiên là thống nhất thuật ngữ, giảm một số khẳng định tuyệt đối và thay vài câu khẩu ngữ bằng mô tả cụ thể. Bài cuối kỳ cần chỉnh nhiều nhất ở cách diễn giải chỉ số; bài giữa kỳ cần tinh giản tóm tắt; bài thường xuyên chủ yếu cần biên tập nhẹ.

## 1. Những điểm nên sửa trước

### 1.1. Bài cuối kỳ: cách diễn giải Pareto k chưa nhất quán với bài giữa kỳ

Vị trí: `final-project/report/bao-cao-cuoi-ky-nhom10.tex:373`, `:886` và `:901`; đối chiếu với `bai-giua-ky/report/report.tex:344` và `:574`.

Các câu “cho biết hậu nghiệm thay đổi nhiều đến đâu”, “k lớn nghĩa là … ước lượng thay đổi nhiều” và “bỏ xe này ra làm hậu nghiệm thay đổi nhiều nhất” khiến người đọc hiểu k là thước đo trực tiếp độ thay đổi của tham số. Bài giữa kỳ diễn đạt thận trọng hơn: dùng k để chẩn đoán phép xấp xỉ PSIS-LOO. Cần đồng bộ ba vị trí trong bài cuối kỳ theo cách đó.

Đề xuất thay đoạn ở dòng 884–888:

> Nhóm dùng phần dư chuẩn hoá để đánh giá mức chênh lệch giữa giá trị quan sát và dự đoán. Chỉ số Pareto k được dùng để chẩn đoán độ ổn định của phép xấp xỉ PSIS-LOO cho từng quan sát. Giá trị k lớn là dấu hiệu cần xem xét thêm quan sát tương ứng; chỉ số này không trực tiếp đo độ thay đổi của hệ số khi loại quan sát đó.

Trong hàng Honda Civic, thay phần sau dấu chấm phẩy bằng: “có k cao nhất mẫu, cần được xem xét thêm trong chẩn đoán PSIS-LOO”. Muốn giữ nhận định về mức thay đổi hậu nghiệm thì cần có kết quả kiểm tra riêng làm căn cứ.

### 1.2. Cả ba bài: “sai số chuẩn” đang mang hai nghĩa

Ví dụ: `bai-thuong-xuyen/report/report.tex:44` và `:81`; `bai-giua-ky/report/report.tex:41` và `:93`; `final-project/report/bao-cao-cuoi-ky-nhom10.tex:474` và `:880`.

“Sai số chuẩn” ở phần OLS chỉ standard error, nhưng “mô hình với sai số chuẩn” lại muốn nói Gaussian errors. Hai cách dùng nằm trong cùng bộ báo cáo nên dễ gây nhầm lẫn.

Nên dùng:

- “sai số có phân phối chuẩn” khi nói về giả định phân phối;
- “sai số chuẩn của ước lượng” khi nói về standard error;
- “độ lệch chuẩn của sai số” khi nói về sigma trong mô hình chuẩn;
- “tham số thang đo” khi nói về sigma của Student-t.

Ví dụ, “giảm từ 1,95 xuống 1,22 khi sai số chuẩn” nên thành “giảm từ 1,95 xuống 1,22 khi dùng mô hình có sai số phân phối chuẩn”. Không thay thế hàng loạt mọi cụm “sai số chuẩn”, vì nhiều chỗ đang dùng đúng nghĩa standard error.

### 1.3. Bài giữa kỳ: “độ phân tán tăng bốn lần” thiếu tên đại lượng

Vị trí: `bai-giua-ky/report/report.tex:35`–`:38`; đối chiếu với công thức và lời giải thích tại `:448`–`:454`, `:473`.

Trong tóm tắt, “độ phân tán” có thể được hiểu là phương sai hoặc độ lệch chuẩn. Phần thân thực tế dùng s_x là độ lệch chuẩn. Với một nhận định định lượng, cần gọi đúng đại lượng ngay trong câu.

Đề xuất:

> Trong điều kiện xấp xỉ đã nêu, khi mức nhiễu không đổi, độ lệch chuẩn của biến giải thích tăng bốn lần giúp giảm độ lệch chuẩn hậu nghiệm của hệ số góc tương đương với việc tăng cỡ mẫu khoảng 16 lần.

Trong tóm tắt có thể chỉ giữ quy luật sigma/(sqrt(n) s_x), chuyển ví dụ “bốn lần – 16 lần” xuống phần thân để giảm tải.

### 1.4. Bài cuối kỳ: góp ý về trung vị đã được xử lý trong bản hiện tại

Vị trí hiện tại: `final-project/report/bao-cao-cuoi-ky-nhom10.tex:957`–`:967`.

Nguồn hiện tại đã viết “trung bình City của M5 không hữu hạn; trung vị không gặp vấn đề này nên nhóm báo cáo trung vị thay cho trung bình”. Câu “trung vị không bị ảnh hưởng” được nhắc trong lần rà soát trước không còn trong nguồn; không coi đây là lỗi còn tồn tại.

Nếu muốn làm rõ hơn đại lượng đang báo cáo, có thể viết:

> Nhóm dùng trung vị có điều kiện để mô tả City. Với M5, phép biến đổi mũ của phân phối Student-t cho kỳ vọng City không hữu hạn, trong khi trung vị có điều kiện vẫn xác định.

Giữ chú thích ở bảng Q4 rằng điểm ước lượng là trung bình hậu nghiệm của trung vị có điều kiện m; không đổi tên cột thành “City trung bình”.

### 1.5. Bài cuối kỳ: câu đối chiếu phương pháp còn tuyệt đối

Vị trí: `final-project/report/bao-cao-cuoi-ky-nhom10.tex:324` và `:338`.

“OLS chỉ cho một ước lượng điểm” làm phần so sánh thiếu cân đối với chính bài thường xuyên, vốn có nhắc sai số chuẩn và khoảng tin cậy. Câu “phải được xấp xỉ bằng lấy mẫu” cũng hẹp hơn phần phương pháp trong bài giữa kỳ, nơi đã trình bày các cách xấp xỉ khác.

Đề xuất thay:

> OLS xác định hệ số bằng cách tối thiểu hoá tổng bình phương phần dư; suy luận theo phương pháp tần suất còn cung cấp sai số chuẩn và khoảng tin cậy dưới các giả định tương ứng.

Và:

> Với lựa chọn tiên nghiệm độc lập đang xét, báo cáo dùng NUTS để xấp xỉ hậu nghiệm bằng lấy mẫu.

Câu thứ hai mô tả đúng lựa chọn của nhóm mà không biến nó thành yêu cầu chung cho mọi phương pháp tính.

## 2. Góp ý theo từng bài

### Bài thường xuyên

Đây là bài có giọng viết tự nhiên nhất. Nên giữ ngôi “tôi” và ví dụ ETL; không cần đổi thành giọng vô nhân xưng cho toàn bài.

Các chỉnh sửa nhỏ:

| Vị trí trong `bai-thuong-xuyen/report/report.tex` | Hiện tại | Gợi ý |
| --- | --- | --- |
| 29 | “Đổi lại cho các ưu điểm này” | “Để sử dụng mô hình, người dùng cần…” |
| 109 | “tổng số dư bình phương” | “tổng bình phương phần dư”, thống nhất với các bài khác |
| 204 | “Ước lượng được khi có ít dữ liệu” | “Hỗ trợ ổn định ước lượng khi có ít dữ liệu” |
| 259 | “Đây là chỗ cách tiếp cận Bayes có lợi rõ nhất” | “Đây là một lợi ích của cách tiếp cận Bayes trong bài toán đang xét” |
| 384 | “điểm thêm của cách Bayes là cho độ bất định đầy đủ” | “cách Bayes biểu diễn đồng thời sự bất định của hệ số từng nhóm và tham số của phân phối chung” |
| 389 | “mỗi lần cập nhật cho ngay một phân phối đầy đủ” | “mỗi lần cập nhật thu được một phân phối hậu nghiệm để tính xác suất và khoảng dự đoán” |

Ý về lợi ích của tiên nghiệm khi mẫu nhỏ và sự gần nhau giữa trung bình hậu nghiệm với OLS lặp ở các dòng 295–300, 326–330 và phần ưu điểm. Có thể giữ phần giải thích chính ở chương so sánh, rút phần lưu ý trong công việc còn một câu dẫn chiếu. Đây là lựa chọn tinh giản, không phải lỗi nội dung.

### Bài giữa kỳ

Điểm mạnh là các mục chỉ rõ đặc điểm mẫu ảnh hưởng đến bước ước lượng nào. Nên giữ chuỗi giải thích này và bảng tổng hợp.

Tóm tắt hiện đưa đồng thời bảy bước, bốn đại lượng, một công thức xấp xỉ, hai quy đổi định lượng và hai kết quả mô phỏng. Người đọc chưa có ngữ cảnh sẽ khó nhận ra ý chính. Có thể giữ quy trình, cơ chế qua các thống kê đủ và một minh hoạ ngoại lai; chuyển các con số 0,14–0,90 và quy đổi 16 lần về phần thân.

Các câu nên chỉnh:

- Dòng 29–31: “các mô phỏng, chủ yếu trên dữ liệu sinh từ … và một mô phỏng hai biến giải thích cho đa cộng tuyến” có nhiều bổ ngữ chen giữa. Tách thành: “Phần lớn mô phỏng dùng dữ liệu sinh từ y = 1 + 2x + epsilon. Riêng mô phỏng đa cộng tuyến dùng hai biến giải thích.”
- Dòng 226–227: “Đưa về dạng bình phương đủ” có thể viết thành “Hoàn thành bình phương theo beta”, thuận với cách mô tả thao tác đại số.
- Dòng 545–546: “kéo cả đường hồi quy … ta lại tưởng là chắc chắn” hơi khẩu ngữ. Đổi thành: “Một điểm ngoại lai có thể làm lệch đường hồi quy trong khi khoảng hậu nghiệm vẫn hẹp, khiến độ bất định bị diễn giải quá lạc quan.”
- Dòng 674–675: “Cỡ mẫu quyết định ảnh hưởng tương đối của tiên nghiệm” mạnh hơn các điều kiện ở phần thân. Đổi thành: “Khi cấu trúc thiết kế và mức nhiễu tương đối ổn định, cỡ mẫu ảnh hưởng đến vai trò tương đối của tiên nghiệm và độ rộng hậu nghiệm.”

### Bài cuối kỳ

Điểm mạnh là phần tóm tắt và Q4 đã ghi rõ cấu hình xe; phần kết luận phân biệt được kiểm tra trong mẫu với đánh giá trên dữ liệu độc lập. Nên giữ các điều kiện này khi rút gọn.

Ngoài các mục ưu tiên ở trên, nên chỉnh:

| Vị trí trong `final-project/report/bao-cao-cuoi-ky-nhom10.tex` | Điểm cần cân nhắc | Gợi ý |
| --- | --- | --- |
| 70 | “tách được vai trò” dễ gợi ý đã xác định riêng tác động của các biến | “khảo sát mối liên hệ của từng biến với City khi đã xét các biến còn lại” |
| 741 | “đều tái tạo tốt mức trung bình … với p-value…” kết luận khá dứt khoát từ một kiểm tra | “Kiểm tra theo thống kê trung bình chưa cho thấy chênh lệch rõ giữa dữ liệu mô phỏng và quan sát…” |
| 832–834 | “khả năng ngược lại … gần như bị loại trừ” | “Trong M2, xác suất hậu nghiệm để xe Mỹ có trung vị City cao hơn ở cùng công suất là 0,003” |
| 838–840 | “phần lớn khoảng cách ban đầu …” vẫn dễ gợi cách hiểu đã phân rã chênh lệch theo nguyên nhân | “Chênh lệch ước lượng giữa hai nhóm thu hẹp khi bổ sung trọng lượng vào mô hình” |
| 877–880 | “mô hình chỉ biết … trở nên bình thường khi mô hình biết chúng nặng” nhân hoá và thiếu cụ thể | “Các xe van có phần dư lớn trong mô hình chỉ dùng công suất, nhưng phần dư giảm khi bổ sung trọng lượng” |
| 903–909 | “máy”, “thân nhẹ”, “trên thân … kg” chưa đồng nhất với phần mô tả dữ liệu | dùng “động cơ”, “trọng lượng thấp”, “trọng lượng … kg” |
| 935–939 | “sai số của M5 có trung vị …” và “chấp nhận được vài xe lệch xa” chưa rõ đại lượng | “Trung vị hậu nghiệm của độ lệch chuẩn sai số, tính trên các mẫu có nu > 2, khoảng 0,45”; sau đó mô tả Student-t gán mật độ lớn hơn cho phần dư lớn |
| 982–988 | “City thật”, “dữ liệu đã thấy” mang giọng nói; “Trong khi đó, M1…” đã được sửa trong nguồn | “City quan sát”, “dữ liệu dùng để ước lượng”; giữ cách chuyển ý hiện tại |

Các kết quả về trọng lượng, chênh lệch xuất xứ và dự đoán 16,6 MPG xuất hiện ở tóm tắt, phần đánh giá và kết luận là hợp lý. Tuy nhiên, kết luận có thể chỉ giữ một kết quả trọng tâm cho mỗi Q; các khoảng và xác suất phụ đã có trong bảng, không cần lặp toàn bộ.

### Bổ sung sau khi đối chiếu lại nguồn hiện tại

1. **Q4 còn kết luận rộng hơn minh hoạ được trình bày** (`final-project/report/bao-cao-cuoi-ky-nhom10.tex:985`–`:989`). Từ việc điểm dự đoán của M1 thấp hơn City của ba xe, câu “chỉ dựa vào công suất là chưa đủ để mô tả nhóm xe mạnh này” đi xa hơn kết quả so sánh điểm đang nêu. Khoảng dự đoán M1 ở bảng Q4 vẫn bao phủ các giá trị 16–18 MPG. Nên viết: “Điểm dự đoán của M1 thấp hơn City quan sát của cả ba xe; phần so sánh mô hình bằng PSIS-LOO ở mục trước cung cấp thêm căn cứ để lựa chọn mô hình có trọng lượng.” Cũng nên thay “mọi dự đoán … đều kém chắc chắn hơn” bằng “cần diễn giải thận trọng vì số xe ở vùng công suất này còn ít”.

2. **Câu kết luận về xuất xứ cần sửa đồng thời ở phần kết luận** (`final-project/report/bao-cao-cuoi-ky-nhom10.tex:1041`). Cụm “nên phần lớn khoảng cách đi cùng với việc xe Mỹ nặng hơn” lặp cách diễn giải tại Q2. Đề xuất: “Chênh lệch ước lượng giữa hai nhóm thu hẹp khi mô hình xét thêm trọng lượng.” Cách viết này khớp trực tiếp với phép so sánh mô hình đã thực hiện.

3. **Nêu trực tiếp xác suất thay cho “chưa loại trừ khả năng không có liên hệ”** (`final-project/report/bao-cao-cuoi-ky-nhom10.tex:809`–`:811`). Đề xuất: “Xác suất hậu nghiệm để hệ số công suất âm là 0,94; tuy nhiên, HDI 95% vẫn chứa 0, cho thấy dấu của hệ số còn bất định trong mô hình M5.” Câu này bám các đại lượng đã báo cáo và tránh khiến người đọc hiểu HDI như kết quả kiểm định một giả thuyết điểm.

4. **Không thay mọi từ “thật” hoặc “đầy đủ” một cách máy móc.** “Giá trị thật của hệ số” trong mô phỏng, “hạng cột đầy đủ” và “phân phối có điều kiện đầy đủ” là các cách dùng có nghĩa rõ. Chỉ đổi “dữ liệu thật” thành “dữ liệu quan sát” khi cần thống nhất văn phong; chỉ giảm “đầy đủ” khi đó là lời khẳng định bao quát về chất lượng suy luận.

Một phương án rút gọn tóm tắt bài giữa kỳ, để người đọc nắm ý chính trước khi gặp các con số chi tiết:

> Bài viết trình bày quá trình ước lượng mô hình hồi quy tuyến tính Bayes và giải thích ảnh hưởng của đặc điểm mẫu dữ liệu đến từng bước ước lượng. Quy trình gồm chuẩn bị dữ liệu, chọn hàm hợp lý và tiên nghiệm, tính hậu nghiệm, chẩn đoán hội tụ khi dùng MCMC, kiểm tra mô hình, suy luận và dự đoán. Công thức hậu nghiệm và dữ liệu mô phỏng được dùng để minh hoạ cơ chế ảnh hưởng của cỡ mẫu, mức nhiễu, độ phân tán, tương quan và thang đo của các biến giải thích, cùng điểm ngoại lai và phạm vi quan sát.
>
> Trong mô hình có sai số phân phối chuẩn và tiên nghiệm cố định, dữ liệu đi vào hậu nghiệm qua n, XᵀX, Xᵀy và yᵀy. Khi thông tin từ dữ liệu chiếm ưu thế và các điều kiện xấp xỉ được đáp ứng, độ lệch chuẩn hậu nghiệm của hệ số góc xấp xỉ σ/(√n sₓ). Các mô phỏng minh hoạ sự gia tăng độ bất định khi các biến giải thích tương quan mạnh và ảnh hưởng của điểm ngoại lai đến ước lượng. Kết quả cho thấy cần lựa chọn tiên nghiệm theo thang đo, kiểm tra giả định mô hình và giới hạn phạm vi dự đoán theo dữ liệu đã quan sát.

Phương án rút gọn này đã được áp dụng vào nguồn LaTeX, có điều chỉnh nhẹ về câu chữ. Các kết quả định lượng chi tiết vẫn giữ ở phần thân bài.

## 3. Nguyên tắc biên tập chung

- Giữ “tôi” trong hai bài cá nhân và “nhóm” trong bài cuối kỳ. Dùng “ta” ở phần dẫn xuất khi cần hướng dẫn phép tính.
- Dùng thuật ngữ tiếng Việt và giải thích tiếng Anh ở lần xuất hiện đầu; sau đó dùng nhất quán. Phần văn xuôi ưu tiên “mã nguồn”, “chương trình”, “giá trị quan sát”; giữ nguyên tên hàm, tên biến và đường dẫn.
- Mỗi đoạn kết quả nên theo thứ tự: điều kiện so sánh, đại lượng được ước lượng, kết quả, ý nghĩa. Các đoạn Q4 hiện đã làm khá tốt.
- Đặt điều kiện ngay cạnh nhận định định lượng; tránh để người đọc phải tìm điều kiện ở chương trước.
- Giảm các từ “chỉ”, “luôn”, “phải”, “đầy đủ”, “quyết định” khi câu thực tế chỉ mô tả lựa chọn trong báo cáo hoặc kết quả trong một điều kiện cụ thể.

Các góp ý biên tập đã được áp dụng vào cả ba báo cáo, gồm thuật ngữ, tóm tắt giữa kỳ, diễn giải Pareto k, so sánh OLS và cách trình bày kết quả Q1–Q4. Phương trình, số liệu kết quả và mã nguồn phân tích được giữ nguyên. File `review.md` cũ được giữ nguyên; những đánh giá lịch sử trong đó về thiếu bài cá nhân, tên giữ chỗ hoặc thiếu khai báo AI không phản ánh bản nguồn được đọc trong lần rà soát này.


## 4. Kiểm tra sau biên tập

Cả ba báo cáo đã biên dịch thành công bằng XeLaTeX qua latexmk, sử dụng biber-arm64: bài thường xuyên 15 trang, bài giữa kỳ 24 trang và bài cuối kỳ 39 trang. Nhật ký LaTeX không có cảnh báo tràn dòng, tham chiếu hoặc trích dẫn chưa xác định. Bộ chuyển PDF còn báo cảnh báo về độ phân giải ảnh JPEG và đích trang đầu trùng tên.

Đã đối chiếu để xác nhận các khối phương trình, mã Python trong báo cáo, định danh nhãn và số liệu trong toàn bộ bảng được giữ nguyên. Đã kiểm tra trực quan trang tóm tắt giữa kỳ và trang chứa bảng ngoại lai cuối kỳ; không thấy chữ hoặc bảng bị cắt. Chưa kiểm tra trực quan toàn bộ các trang PDF.
