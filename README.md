# Hồi quy tuyến tính Bayes — Xe mới tại Mỹ năm 1993

Code cho báo cáo cuối kỳ, theo outline `Báo cáo cuối kỳ_ Hồi quy tuyến tính Bayes – Xe mới tại Mỹ năm 1993.pdf`.
Python + PyMC + ArviZ, seed 2026, NUTS 4 chuỗi × 2000 vòng (1000 warm-up).

## Chạy

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python build_notebook.py        # chạy toàn bộ (~10 phút), ghi bayes_cars_1993.ipynb
```

Hoặc chạy từng module theo thứ tự: `02 → 03 → 04 → 01 → 05`, ví dụ `.venv/bin/python analysis/02_data_eda.py`.

PyTensor không biên dịch được C trên toolchain macOS này (clang báo lỗi `-ld64`), nên `common.py` đặt
`PYTENSOR_FLAGS=cxx=` để chạy backend Python. Chậm hơn nhưng đủ nhanh với 93 dòng.

## Module ↔ outline

| Module | Người phụ trách | Mục trong báo cáo | Đầu ra chính |
| --- | --- | --- | --- |
| `analysis/02_data_eda.py` | TV2 | Ch.2, 3.1–3.3, Q1 (scatterplot) | `data_clean.csv`, `fig_2_6_*`, `tab_3_2_vif.csv`, `tab_3_1_ols.csv` |
| `analysis/03_models.py` | TV3 | 3.4–3.7 | `fig_3_6_prior_predictive.png`, `tab_3_7_sensitivity.csv` |
| `analysis/04_sampling.py` | TV4 | 4.2–4.4 | `idata/idata_M1..M5.nc`, `tab_4_3_diagnostics.csv`, `tab_4_4_posterior.csv`, MH tự cài |
| `analysis/01_conjugate.py` | TV1 | 4.1 | `tab_4_1_conjugate_vs_mcmc.csv`, `fig_4_1_conjugate.png` |
| `analysis/05_evaluation.py` | TV5 | 5.1–5.6 (Q1–Q4) | `tab_5_*`, `fig_5_*` |
| `analysis/common.py` | chung | — | đường dẫn, seed, chuẩn hoá, định nghĩa M1–M5 |

Mọi kết quả nằm trong `outputs/`: `figures/` (tên hình theo mục, ví dụ `fig_2_6_scatter.png`), `tables/` (CSV),
`idata/` (NetCDF), và `results.json` (các con số chính để viết báo cáo).

## Quyết định mô hình hoá

- **Đơn vị City**: giá trị 15–46, Geo Metro = 46 → xem là MPG (càng cao càng tiết kiệm), như mục 2.4.
- **Biến phản hồi**: log(City), chuẩn hoá. So với City gốc, log-likelihood trên thang City tốt hơn
  (−246 so với −264, `tab_3_3_response_scale.csv`). Dự đoán được đổi ngược về MPG.
- **Biến giải thích**: HP và Weight chuẩn hoá; USA giữ 0/1.
- **Prior** (thang chuẩn hoá): β ~ N(0, 2.5²), σ ~ Half-Normal(1). Độ nhạy: flat N(0, 100²), tight N(0, 0.5²).
- **M5** = mô hình tốt nhất trong M1–M4 theo PSIS-LOO (tự chọn trong `04_sampling.py`), likelihood Student-t,
  ν ~ Gamma(2, 0.1).
- **Q4**: với mô hình có Weight, “xe 300 hp” lấy trọng lượng trung bình của 3 xe thật ≥ 295 hp (1681 kg).
# special-topic-2-bayes
