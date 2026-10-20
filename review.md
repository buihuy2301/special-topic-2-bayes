# Rà soát bài làm theo yêu cầu của giảng viên

Ngày rà soát: 20/10/2026.

## 1. Kết luận chung

Ba bài hiện tại bám khá sát yêu cầu về nội dung. Bài giữa kỳ đáp ứng tốt trọng tâm giải thích quá trình học và ảnh hưởng của mẫu dữ liệu. Bài cuối kỳ đã có đầy đủ các phần chuyên môn chính nhưng **chưa nên nộp nguyên trạng**, vì còn thiếu thông tin phân công thành viên và khai báo AI, đồng thời cần chỉnh một số diễn giải thống kê.

Có phần làm sâu hơn mức cần thiết, nhất là ở bài thường xuyên và các thuật toán phụ trong bài cuối kỳ. Không cần bổ sung thêm mô hình; nên ưu tiên hoàn thiện yêu cầu bắt buộc, sửa độ chính xác và tinh giản trình bày.

Phạm vi rà soát: đọc nội dung nguồn LaTeX, kiểm tra văn bản PDF, đối chiếu tài liệu đề Q_10 và xem các phần code chính. Chưa chạy lại toàn bộ chương trình và chưa kiểm tra trực quan từng trang PDF. Đây không phải cam kết về điểm số hay xác nhận khả năng tái lập toàn bộ kết quả.

## 2. Mức độ đáp ứng của từng bài

| Bài | Hiện trạng | Mức đáp ứng | Mức độ cần tinh giản |
| --- | --- | --- | --- |
| Thường xuyên | 14 trang PDF | Đủ các ý: khái niệm, ý nghĩa ứng dụng, liên hệ công việc và so sánh với hồi quy thông thường | Hơi dài; có thể rút phần công thức dạng đóng, Ridge, MCMC và số liệu cuối kỳ |
| Giữa kỳ | 20 trang PDF | Bám đề tốt; có quy trình ước lượng, công thức, đặc điểm mẫu và liên hệ với từng bước | Độ sâu hợp lý với yêu cầu “chi tiết nhất”; có thể rút phần liệt kê thuật toán và minh hoạ cuối kỳ |
| Cuối kỳ | 30 trang PDF | Có dữ liệu, mô hình hoá, ước lượng Bayes, đánh giá và trả lời Q1–Q4; có code có comment và dữ liệu | Có thể chuyển thuật toán phụ, dẫn xuất dài và đồ thị chẩn đoán lặp lại xuống phụ lục |

Giảng viên không quy định số trang. Các nhận xét về độ dài là đề xuất biên tập, không phải điều kiện bắt buộc. Python/PyMC phù hợp vì đề cho phép mọi phần mềm và ngôn ngữ; tài liệu R là hướng dẫn tham khảo.

## 3. Những việc cần hoàn thiện trước khi nộp

### 3.1. Phân công thành viên trong PDF cuối kỳ — bắt buộc

**Vị trí:** `bai-cuoi-ky/report/report.tex`, trang bìa và phụ lục “Code và dữ liệu”.

Trang bìa còn các tên giữ chỗ “Thành viên 2”, “Thành viên 3”, … Bảng module mới gắn công việc với TV1–TV5, chưa mô tả rõ đầu việc tìm hiểu lý thuyết và lập trình của từng thành viên. Chưa xác định trưởng nhóm và công việc của trưởng nhóm.

Yêu cầu C của giảng viên bắt buộc mô tả các đầu việc này ngay trong PDF. Bảng trong README không thay thế được phần phân công trong bài luận.

**Cách xử lý:** bổ sung bảng gồm họ tên, mã học viên, vai trò, đầu việc lý thuyết, đầu việc lập trình và sản phẩm thực tế. Ghi riêng đóng góp của trưởng nhóm nếu có, chẳng hạn điều phối, tích hợp code, rà soát kết quả hoặc biên tập báo cáo. Nội dung phải phản ánh đúng công việc đã thực hiện; không suy ra đóng góp thực tế chỉ từ cấu trúc module.

### 3.2. Khai báo AI đã tham khảo — bắt buộc khi có sử dụng

**Vị trí:** cả ba báo cáo.

Chưa thấy mục khai báo AI trong ba PDF. Yêu cầu B cho phép sử dụng AI nhưng phải ghi rõ các AI đã tham khảo.

**Cách xử lý:** thêm một mục ngắn ghi tên công cụ thực sự đã dùng, phạm vi hỗ trợ và phần người học đã tự kiểm tra. Không tự điền tên mô hình hoặc phiên bản khi chưa xác định được.

### 3.3. Căn cứ xác định đơn vị City — cần làm rõ

**Vị trí:** bài cuối kỳ, mục “Đơn vị nhiên liệu” và “Hạn chế”.

Tài liệu PDF của đề ghi lít/100 km, tiêu đề CSV ghi km/100L, còn báo cáo dùng MPG. Việc phát hiện mâu thuẫn là đúng, nhưng lập luận từ chiều tương quan giữa trọng lượng và City chưa đủ để xác nhận đơn vị.

Tài liệu chính thức của `MASS::Cars93` ghi các biến hiệu suất nhiên liệu tương ứng theo MPG. Nên đối chiếu các dòng xe và giá trị cụ thể với bộ dữ liệu đó, rồi trình bày bằng chứng cho cách diễn giải đơn vị. Không chỉ dựa vào việc kết quả có vẻ hợp lý về mặt thực tế.

Nguồn đối chiếu: [MASS::Cars93](https://stat.ethz.ch/R-manual/R-devel/library/MASS/html/Cars93.html).

### 3.4. Giảm diễn giải mang nghĩa nhân quả — cần sửa

**Vị trí:** tóm tắt, phần hậu nghiệm, Q1, Q2 và kết luận bài cuối kỳ.

Các câu như “trọng lượng quyết định”, “phần lớn ảnh hưởng của công suất thực ra là ảnh hưởng của trọng lượng” và “xe Mỹ tốn nhiên liệu chủ yếu vì nặng hơn” mạnh hơn mức một phân tích hồi quy trên dữ liệu quan sát có thể chứng minh.

**Gợi ý diễn đạt:**

> Trong mẫu và các mô hình đang xét, trọng lượng có liên hệ mạnh với City. Khi bổ sung trọng lượng, độ lớn hệ số công suất và chênh lệch giữa hai nhóm xuất xứ giảm.

Việc thêm biến làm hệ số thay đổi chưa tự nó chứng minh cơ chế nhân quả hay tỷ lệ tác động được giải thích bởi biến đó.

### 3.5. Phân biệt trung vị, trung bình và tham số thang đo — cần sửa

**Vị trí:** `bai-cuoi-ky/analysis/05_evaluation.py`, các bảng/hình dự đoán và phần diễn giải trong báo cáo.

Hàm `predict_mpg(..., kind="mu")` đang đổi ngược vị trí trên thang log bằng phép mũ. Với mỗi bộ tham số, đại lượng này là trung vị có điều kiện trên thang City, không phải trung bình số học có điều kiện. Trung bình các giá trị này qua mẫu hậu nghiệm cũng không tự trở thành kỳ vọng dự đoán của City.

Với sai số chuẩn trên thang log, kỳ vọng trên thang gốc cần hiệu chỉnh phương sai. Với Student-t trên thang log, kỳ vọng của biến sau phép mũ không hữu hạn; vì vậy không nên gọi các giá trị hiện tại là “City trung bình” hoặc “HDI của trung bình”. Có thể báo cáo trung vị dự đoán, các phân vị và khoảng dự đoán, đồng thời ghi rõ đại lượng đang tính.

Ngoài ra, `sigma` của Student-t là tham số thang đo. Khi bậc tự do lớn hơn 2, độ lệch chuẩn là `sigma * sqrt(nu / (nu - 2))`; với bậc tự do không quá 2, phương sai không hữu hạn. Không nên gọi `sigma` của M5 là độ lệch chuẩn nhiễu hoặc so trực tiếp nó với độ lệch chuẩn của mô hình chuẩn để kết luận nhiễu giảm.

Nguồn định nghĩa: [PyMC StudentT](https://www.pymc.io/projects/docs/en/stable/api/distributions/generated/pymc.StudentT.html).

### 3.6. Nói rõ phạm vi kiểm tra dự đoán Q4 — cần sửa

**Vị trí:** bài cuối kỳ, Q4, tóm tắt và kết luận.

Ba xe gần 300 hp đã nằm trong dữ liệu dùng để học mô hình. Việc giá trị thật nằm trong khoảng dự đoán là kiểm tra độ phù hợp trong mẫu, chưa phải kiểm chứng khả năng dự đoán cho xe mới.

M1 trả lời tình huống chỉ biết HP. M5 cần thêm xuất xứ và trọng lượng; kết quả 16,6 MPG phụ thuộc vào giả định xe Mỹ nặng 1681 kg. Giả định đã được nêu nhưng cần giữ rõ trong mọi chỗ tóm tắt kết quả, tránh trình bày thành dự đoán chung cho mọi xe 300 hp.

### 3.7. Giới hạn kết luận cho Open Road — nên sửa

**Vị trí:** bài cuối kỳ, phần trả lời Q1.

Tương quan City–Open Road cao không đủ để khẳng định mọi kết luận hồi quy cho City cũng áp dụng cho Open Road. Nên viết rằng hai biến có liên hệ mạnh và có thể có xu hướng tương tự; muốn kết luận định lượng cho Open Road cần phân tích riêng.

## 4. Phần nên giữ và phần có thể rút gọn

### Bài thường xuyên

- Giữ: giải thích likelihood–prior–posterior, ý nghĩa xác suất, ứng dụng trong công việc kỹ sư dữ liệu ngân hàng, bảng so sánh và hạn chế.
- Rút gọn: dẫn xuất hậu nghiệm dạng đóng, liên hệ Ridge, danh sách thuật toán MCMC và số liệu chi tiết từ bài cuối kỳ.
- Ưu tiên giọng viết cá nhân: nêu một bài toán công việc cụ thể, dữ liệu cần có, lợi ích kỳ vọng và cách đánh giá tính khả thi.

### Bài giữa kỳ

- Giữ: các bước học, công thức hậu nghiệm, vai trò của thống kê đủ và chương phân tích đặc điểm mẫu.
- Giữ rõ chuỗi giải thích: đặc điểm dữ liệu → đại lượng/cấu trúc mô hình bị ảnh hưởng → bước ước lượng cần thay đổi → hệ quả với suy luận và dự đoán.
- Có thể rút phần minh hoạ cuối kỳ nếu lặp lại nhiều số liệu; đưa dẫn xuất dài xuống phụ lục.

### Bài cuối kỳ

- Giữ: mô tả dữ liệu, EDA phục vụ Q1–Q3, lựa chọn biến và thang đo, đặc tả prior/likelihood, hậu nghiệm, chẩn đoán, kiểm tra dự đoán và câu trả lời Q1–Q4.
- Chuyển xuống phụ lục: Metropolis–Hastings tự cài, dẫn xuất liên hợp chi tiết và trace/rank plot của mọi mô hình.
- Có thể dùng PSIS-LOO làm tiêu chí chính, chuyển WAIC sang phần bổ sung nếu hai tiêu chí chỉ lặp lại cùng thông tin.
- Chỉ giữ các mô hình mở rộng nếu giải thích được chúng giúp trả lời câu hỏi nào hoặc kiểm tra giả định nào.

## 5. Thứ tự xử lý đề xuất

1. Hoàn thiện tên thành viên, trưởng nhóm và bảng đóng góp thực tế trong PDF cuối kỳ.
2. Bổ sung khai báo AI vào các bài có sử dụng.
3. Làm rõ đơn vị City bằng đối chiếu nguồn dữ liệu.
4. Sửa tên đại lượng dự đoán, diễn giải `sigma` của Student-t và các kết luận nhân quả quá mạnh.
5. Chỉnh phạm vi kết luận Q4 và Open Road.
6. Tinh giản bài thường xuyên, chuyển nội dung phụ của bài cuối kỳ xuống phụ lục.
7. Biên dịch lại PDF, kiểm tra hình/bảng, tham chiếu và sự khớp nhau giữa kết quả code với báo cáo. Nếu thay đổi cách tính đại lượng thì chạy lại phần phân tích liên quan.
8. Chuẩn bị gói nộp cuối kỳ có PDF, dữ liệu, code có comment và hướng dẫn chạy; trưởng nhóm nộp. Hai bài cá nhân nộp riêng theo yêu cầu.

## 6. Lưu ý về tính độc lập của bài cá nhân

Giảng viên quy định các PDF giống nhau trên 80% bị coi là sao chép và chia điểm theo số lượng file. Rà soát này chưa so sánh với bài của các học viên khác nên không thể xác nhận tỷ lệ trùng lặp. Mỗi người cần có lập luận, liên hệ công việc và cách trình bày của riêng mình; thay tên trên cùng một bản bài làm không đáp ứng yêu cầu cá nhân.
