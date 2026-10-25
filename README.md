# special-topic-2-bayes

Bài cuối kỳ môn chuyên đề **Mô hình hồi quy tuyến tính Bayes và ứng dụng** — Nhóm 10, dữ liệu `Q_10`
(xe mới tại Mỹ năm 1993).

| Thư mục | Nội dung |
| --- | --- |
| `cuoi-ky-nhom10/` | Báo cáo `report/bao-cao-cuoi-ky-nhom10.pdf` (nguồn `.tex` cùng thư mục), notebook `bayes_cars_1993.ipynb`, code phân tích `analysis/`, dữ liệu `Q_10/`, kết quả `outputs/` |
| `tai-lieu/` | Slide bài giảng của thầy: `Gioi thieu Thong ke Bayes.pdf`, `Slide_HQTT Bayes.pdf` (hồi quy tuyến tính Bayes) |
| `shared/` | Mẫu trình bày LaTeX dùng chung: `layout.tex`, `preamble.tex`, `meta.tex` (tên môn, giảng viên), `refs.bib`, logo |

Chi tiết cách chạy và các quyết định mô hình hoá: [`cuoi-ky-nhom10/README.md`](cuoi-ky-nhom10/README.md).

## Môi trường Python

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
cd cuoi-ky-nhom10 && ../.venv/bin/python build_notebook.py   # toàn bộ phân tích (~8 phút)
```

## Biên dịch báo cáo

Báo cáo biên dịch từ thư mục `cuoi-ky-nhom10/report/` bằng XeLaTeX:

```bash
cd cuoi-ky-nhom10/report && latexmk -xelatex bao-cao-cuoi-ky-nhom10.tex
latexmk -C            # dọn file trung gian
```

Trên máy này `biber` của TeX Live 2025 báo `extracting arm64 binary with lipo failed`. Cách khắc phục đã
kiểm chứng: tách sẵn bản arm64 một lần rồi chỉ cho latexmk dùng bản đó.

```bash
mkdir -p ~/bin && lipo "$(readlink -f "$(which biber)")" -thin arm64 -output ~/bin/biber-arm64
latexmk -xelatex -e '$biber="~/bin/biber-arm64 %O %S"' bao-cao-cuoi-ky-nhom10.tex
```

## Trình bày chung

- `bao-cao-cuoi-ky-nhom10.tex` đặt `\sharedir` (đường dẫn tới `shared/`), `\figdir` (thư mục hình PNG),
  rồi `\input{\sharedir/layout.tex}`; trang bìa in bằng `\makereporttitlepage`.
- Trang bìa theo mẫu báo cáo môn Các phương pháp ngẫu nhiên (khung viền, tiêu đề in hoa, khối giảng viên/học viên).
- Thông tin riêng của báo cáo khai báo đầu file `.tex`: `\reporttitle`, `\reportname`, `\studentlabel`,
  `\studentname` (mỗi dòng `Họ tên & MSSV`, các dòng cách nhau bằng `\\`). Thông tin chung cả môn ở
  `shared/meta.tex`: `\coursetitle` (tên môn in trên bìa), `\coursename` (header) và `\teachername` (để trống thì
  khối giảng viên bị ẩn).
- `\resultfig[tỉ lệ rộng]{tên file}{chú thích}{nhãn}` lấy `\figdir/<tên file>.png`; hình chưa sinh hiện
  thành khung trống ghi tên file, nên báo cáo vẫn biên dịch được.
- Chương đánh số La Mã, mục/hình/bảng/phương trình đánh số `3.2`, phụ lục đánh số `A.1`.
