# special-topic-2-bayes

Bài làm môn chuyên đề, chủ đề **Mô hình hồi quy tuyến tính Bayes và ứng dụng**. Ba bài dùng chung
một mẫu trình bày LaTeX (cùng mẫu với báo cáo môn Tối ưu hoá).

| Thư mục | Đề bài | Hình thức | Sản phẩm |
| --- | --- | --- | --- |
| `bai-thuong-xuyen/` | Hồi quy tuyến tính Bayes là gì, ý nghĩa ứng dụng, dùng được trong công việc không, ưu nhược điểm so với hồi quy thông thường | Cá nhân | `report/report.pdf` |
| `bai-giua-ky/` | Ước lượng (học) mô hình hồi quy tuyến tính Bayes; phụ thuộc vào đặc điểm nào của mẫu, thể hiện ở các bước ra sao | Cá nhân | `report/report.pdf`, hình mô phỏng do `make_figures.py` sinh |
| `bai-cuoi-ky/` | Áp dụng hồi quy Bayes cho dữ liệu `Q_10` (xe mới tại Mỹ năm 1993) và trả lời các câu hỏi | Nhóm 10 | `report/report.pdf`, notebook `bayes_cars_1993.ipynb` |
| `shared/` | Mẫu trình bày dùng chung: `layout.tex`, `preamble.tex`, `meta.tex` (tên môn, giảng viên), `refs.bib`, logo | | |

## Môi trường Python

Một môi trường dùng chung ở gốc repo:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python bai-giua-ky/make_figures.py          # hình cho bài giữa kỳ (vài giây)
cd bai-cuoi-ky && ../.venv/bin/python build_notebook.py   # toàn bộ phân tích cuối kỳ (~8 phút)
```

## Biên dịch báo cáo

Mỗi báo cáo biên dịch từ thư mục `report/` của nó bằng XeLaTeX:

```bash
cd bai-giua-ky/report && latexmk -xelatex report.tex
latexmk -C            # dọn file trung gian
```

Trên máy này `biber` của TeX Live 2025 báo `extracting arm64 binary with lipo failed`. Cách khắc phục đã
kiểm chứng: tách sẵn bản arm64 một lần rồi chỉ cho latexmk dùng bản đó.

```bash
mkdir -p ~/bin && lipo "$(readlink -f "$(which biber)")" -thin arm64 -output ~/bin/biber-arm64
latexmk -xelatex -e '$biber="~/bin/biber-arm64 %O %S"' report.tex
```

## Trình bày chung

- Mỗi `report.tex` đặt `\sharedir` (đường dẫn tới `shared/`), tuỳ chọn `\figdir` (thư mục hình PNG của
  bài), rồi `\input{\sharedir/layout.tex}`; trang bìa in bằng `\makereporttitlepage`.
- Thông tin riêng từng bài khai báo đầu `report.tex`: `\reporttitle`, `\reportname`, `\studentlabel`,
  `\studentname`. Thông tin chung cả môn ở `shared/meta.tex`: `\coursename` (**tên môn đang là chỗ giữ
  chỗ**) và `\teachername` (để trống thì khối giảng viên bị ẩn).
- `\resultfig[tỉ lệ rộng]{tên file}{chú thích}{nhãn}` lấy `\figdir/<tên file>.png`; hình chưa sinh hiện
  thành khung trống ghi tên file, nên báo cáo vẫn biên dịch được.
- Chương đánh số La Mã, mục/hình/bảng/phương trình đánh số `3.2`, phụ lục đánh số `A.1`.
