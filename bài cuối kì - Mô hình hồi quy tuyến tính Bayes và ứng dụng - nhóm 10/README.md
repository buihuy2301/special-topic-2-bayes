# Bài cuối kì — Mô hình hồi quy tuyến tính Bayes và ứng dụng — Nhóm 10

Đề tài: hồi quy tuyến tính Bayes cho dữ liệu xe mới tại Mỹ năm 1993 (bộ dữ liệu `Q_10`).

## Cấu trúc

```
Báo cáo cuối kì - ... - nhóm 10.pdf   ← báo cáo chính
README.md
code/
├── Q_10/                    dữ liệu gốc (CSV + mô tả PDF)
├── analysis/                mã nguồn Python, chạy theo thứ tự 01 → 05
│   ├── common.py            đường dẫn, seed, chuẩn hoá, định nghĩa M1–M5
│   ├── 01_data_eda.py       Ch.2, 3.1–3.3     (Bùi Quang Huy)
│   ├── 02_models.py         3.4–3.7           (Nguyễn Thị Bích Ngọc)
│   ├── 03_sampling.py       4.2–4.4           (Nguyễn Thu Ngân)
│   ├── 04_conjugate.py      4.1               (Nguyễn Thục Anh)
│   └── 05_evaluation.py     5.1–5.6, Q1–Q4    (Nguyễn Hồng Phúc)
├── bayes_cars_1993.ipynb    notebook gộp toàn bộ phân tích, đã chạy sẵn kết quả
├── build_notebook.py        sinh lại notebook từ các module
├── requirements.txt
└── outputs/
    ├── figures/             hình trong báo cáo (tên theo mục, ví dụ fig_2_5_scatter.png)
    ├── tables/              bảng kết quả (CSV)
    ├── data_clean.csv
    └── results.json         các con số chính dùng trong báo cáo
```

Các file mẫu hậu nghiệm `outputs/idata/*.nc` (~125 MB) không kèm theo; chạy lại code sẽ sinh ra.

## Chạy lại

Python 3.12 + PyMC + ArviZ, seed 2026, NUTS 4 chuỗi × 2000 vòng (1000 warm-up). Trong thư mục `code/`:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build_notebook.py    # chạy toàn bộ (~8 phút), ghi bayes_cars_1993.ipynb
```

Hoặc chạy từng module: `.venv/bin/python analysis/01_data_eda.py`, rồi 02 → 05.
