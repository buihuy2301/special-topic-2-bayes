# Biên dịch báo cáo

Báo cáo viết bằng LaTeX theo cùng mẫu với `../../Optimization/report/`, biên dịch bằng
XeLaTeX vì cần font Unicode đầy đủ dấu tiếng Việt.

## Biên dịch

Chạy từ trong thư mục `report/`:

```bash
latexmk -xelatex report.tex
latexmk -C            # dọn file trung gian
```

Trên máy này `biber` của TeX Live 2025 báo `extracting arm64 binary with lipo failed`.
Cách khắc phục đã kiểm chứng: tách sẵn bản arm64 rồi chỉ cho latexmk dùng bản đó.

```bash
lipo "$(readlink -f "$(which biber)")" -thin arm64 -output ~/bin/biber-arm64
latexmk -xelatex -e '$biber="~/bin/biber-arm64 %O %S"' report.tex
```

## Trình bày

- Lớp `report`, chương đánh số La Mã, mục/hình/bảng đánh số `5.2`; phụ lục đánh số `A.1`.
- Trang bìa lấy thông tin từ các macro đầu `report.tex`: `\coursename`, `\reportname`,
  `\reporttitle`, `\studentname`, `\teachername`. **Tên môn và tên thành viên hiện là chỗ
  giữ chỗ (TV1–TV5)**; sửa ở đó, không sửa rải rác trong thân bài. `\teachername` để trống
  thì khối giảng viên bị ẩn.
- Đầu trang: tên báo cáo bên trái, tên trường và tên môn bên phải; chân trang: số trang.

## Hình

`\resultfig[tỉ lệ rộng]{tên file}{chú thích}{nhãn}` lấy hình PNG từ `../outputs/figures/`,
do notebook sinh ra. Hình nào chưa có sẽ hiện thành khung trống ghi tên file, nên báo cáo
vẫn biên dịch được. Chạy lại `../build_notebook.py` rồi biên dịch lại là hình cập nhật.
Các con số trong bảng lấy từ `../outputs/results.json` và `../outputs/tables/`.
