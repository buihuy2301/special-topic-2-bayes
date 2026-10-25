"""Merge the five modules into one notebook and run it top to bottom.

Usage: .venv/bin/python build_notebook.py [--no-exec]
Order follows the data flow: 01 → 02 → 03 → 04 (needs idata_M1) → 05.
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent
ORDER = ["01_data_eda", "02_models", "03_sampling", "04_conjugate", "05_evaluation"]
NB_PATH = ROOT / "bayes_cars_1993.ipynb"


def cells_from_script(path):
    """Split a `# %%` script into notebook cells; `# %% [markdown]` cells become markdown."""
    cells, kind, buf = [], None, []

    def flush():
        text = "\n".join(buf).strip("\n")
        if kind == "markdown":
            text = "\n".join(line[2:] if line.startswith("# ") else line.lstrip("#") for line in text.splitlines())
            cells.append(nbformat.v4.new_markdown_cell(text))
        elif kind == "code" and text:
            cells.append(nbformat.v4.new_code_cell(text))

    for line in path.read_text().splitlines():
        if line.startswith("# %%"):
            flush()
            kind, buf = ("markdown" if "[markdown]" in line else "code"), []
        else:
            buf.append(line)
    flush()
    return cells


nb = nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_markdown_cell(
    "# Hồi quy tuyến tính Bayes — Xe mới tại Mỹ năm 1993\n\n"
    "Notebook chung, ghép từ 5 module trong `analysis/` (chạy `build_notebook.py` để tạo lại). "
    "Biến phản hồi: City (MPG, mô hình hoá trên thang log), biến giải thích chính: Horsepower."))
# Relative to the notebook's folder, so the notebook keeps working wherever the
# repository is cloned.
nb.cells.append(nbformat.v4.new_code_cell('import sys\nsys.path.insert(0, "analysis")'))
for name in ORDER:
    nb.cells.extend(cells_from_script(ROOT / "analysis" / f"{name}.py"))
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}

if "--no-exec" not in sys.argv:
    NotebookClient(nb, timeout=1800, kernel_name="python3",
                   resources={"metadata": {"path": str(ROOT)}}).execute()
nbformat.write(nb, NB_PATH)
print("wrote", NB_PATH)
