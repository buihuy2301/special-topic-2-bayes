"""Shared config, data access and model definitions for every module.

Every module imports this file first, so the PyTensor flag below is set
before PyMC is imported anywhere.
"""
import json
import os
import re
import warnings
from pathlib import Path

# The C backend fails to link on this macOS toolchain (clang rejects `-ld64`);
# the pure-Python backend is slower but fine for 93 rows.
os.environ.setdefault("PYTENSOR_FLAGS", "cxx=")
warnings.filterwarnings("ignore", category=FutureWarning)

import matplotlib

try:  # inside Jupyter: show figures inline; as a script: write files only
    get_ipython  # noqa: B018
    IN_NOTEBOOK = True
except NameError:
    IN_NOTEBOOK = False
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SEED = 2026
ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = ROOT / "Q_10" / "American New Cars of 1993.csv"
OUT = ROOT / "outputs"
FIG = OUT / "figures"
TAB = OUT / "tables"
IDATA = OUT / "idata"
CLEAN_CSV = OUT / "data_clean.csv"
RESULTS = OUT / "results.json"
for _d in (FIG, TAB, IDATA):
    _d.mkdir(parents=True, exist_ok=True)

# Sampler settings from the outline (section 4.2): 4 chains x 2000 draws, 1000 warm-up.
SAMPLE_KW = dict(draws=2000, tune=1000, chains=4, cores=4, random_seed=SEED,
                 progressbar=False, mp_ctx="fork",
                 idata_kwargs={"log_likelihood": True})

plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
                     "axes.spines.top": False, "axes.spines.right": False})

COLOR = {"USA": "#c0392b", "Nước ngoài": "#2471a3"}


_FIG_NUMBER = re.compile(r"^Hình [0-9.]+[a-z]? — ")


def savefig(fig, name):
    # Drop "Hình x.y — ..." titles: the report's LaTeX captions number and describe
    # the figures. Plain subplot titles (model names, variables) stay.
    if fig._suptitle is not None and _FIG_NUMBER.match(fig._suptitle.get_text()):
        fig._suptitle.remove()
        fig._suptitle = None
    for ax in fig.axes:
        if _FIG_NUMBER.match(ax.get_title()):
            ax.set_title("")
    fig.savefig(FIG / name)
    if IN_NOTEBOOK:
        from IPython.display import display
        display(fig)
    plt.close(fig)
    print("saved", FIG / name)


# ---------------------------------------------------------------- data

RENAME = {
    "Car Name": "name", "Type": "type",
    "Min Price ($US1,000)": "price_min", "Med Price ($US1,000)": "price",
    "Max Price ($US1,000)": "price_max",
    "City (km/100L)": "city", "Open Road (km/100L)": "open_road",
    "Airbag": "airbag", "Drive train": "drive_train", "Cylinders": "cylinders",
    "Engine Size (Litres)": "engine_size", "Horsepower (HP)": "hp",
    "Revs at max power (RPM)": "rpm_max", "Revs at cruising speed (RPM)": "rpm_cruise",
    "Manual transmission avaiable": "manual", "Fuel tank (Litres)": "fuel_tank",
    "Passenger Capacity (persons)": "passengers", "Length (cm)": "length",
    "Wheelbase (cm)": "wheelbase", "Width (cm)": "width", "u-turn space (m)": "uturn",
    "rear seat room (cm)": "rear_seat", "luggage capacity (m3)": "luggage",
    "Weight (kg)": "weight", "USA or Foreign car": "usa",
}
TYPE_LABEL = {1: "Small", 2: "Midsize", 3: "Large", 4: "Compact", 5: "Sporty", 6: "Van"}


def load_clean():
    d = pd.read_csv(CLEAN_CSV)
    d["origin"] = np.where(d["usa"] == 1, "USA", "Nước ngoài")
    return d


class Scaler:
    """Standardises predictors and log(City) using the sample mean/sd."""

    def __init__(self, d):
        self.hp_mu, self.hp_sd = d["hp"].mean(), d["hp"].std()
        self.w_mu, self.w_sd = d["weight"].mean(), d["weight"].std()
        logy = np.log(d["city"])
        self.y_mu, self.y_sd = logy.mean(), logy.std()

    def hp(self, x):
        return (np.asarray(x, float) - self.hp_mu) / self.hp_sd

    def w(self, x):
        return (np.asarray(x, float) - self.w_mu) / self.w_sd

    def y(self, city):
        return (np.log(np.asarray(city, float)) - self.y_mu) / self.y_sd

    def to_mpg(self, z):
        return np.exp(self.y_mu + self.y_sd * np.asarray(z))


# ---------------------------------------------------------------- models

# Terms in each candidate model (section 3.4). M5 reuses the terms of the
# best of M1-M4 with a Student-t likelihood and is built in 04_sampling.
MODEL_TERMS = {
    "M1": ["hp"],
    "M2": ["hp", "usa"],
    "M3": ["hp", "usa", "hp_usa"],
    "M4": ["hp", "weight", "usa"],
}
MODEL_FORMULA = {
    "M1": "City ~ HP",
    "M2": "City ~ HP + USA",
    "M3": "City ~ HP + USA + HP×USA",
    "M4": "City ~ HP + Weight + USA",
}

# Prior sd for the coefficients on the standardised scale (section 3.6-3.7).
PRIOR_SD = {"flat": 100.0, "weak": 2.5, "tight": 0.5}


def design(d, sc, terms, hp=None, weight=None, usa=None):
    """Columns of the design matrix (without intercept) for the given terms.

    Values passed explicitly override the columns of `d`; with `d=None`, a variable
    that is not passed sits at its sample mean (z = 0) or at USA = 0.
    """
    def pick(col, value):
        if value is not None:
            return value
        return d[col] if d is not None else None

    hp_v, w_v, u_v = pick("hp", hp), pick("weight", weight), pick("usa", usa)
    hp_z = sc.hp(hp_v) if hp_v is not None else 0.0
    w_z = sc.w(w_v) if w_v is not None else 0.0
    u = np.asarray(u_v if u_v is not None else 0.0, float)
    hp_z, w_z, u = np.broadcast_arrays(hp_z, w_z, u)
    cols = {"hp": hp_z, "weight": w_z, "usa": u, "hp_usa": hp_z * u}
    return np.column_stack([cols[t] for t in terms])


def build_model(d, sc, terms, prior="weak", likelihood="normal"):
    import pymc as pm

    X = design(d, sc, terms)
    y = sc.y(d["city"])
    coords = {"term": terms, "obs": d["name"].to_numpy()}
    with pm.Model(coords=coords) as model:
        Xd = pm.Data("X", X, dims=("obs", "term"))
        b0 = pm.Normal("b0", 0, PRIOR_SD[prior])
        b = pm.Normal("b", 0, PRIOR_SD[prior], dims="term")
        sigma = pm.HalfNormal("sigma", 1)
        mu = pm.Deterministic("mu", b0 + pm.math.dot(Xd, b), dims="obs")
        if likelihood == "student":
            nu = pm.Gamma("nu", 2, 0.1)
            pm.StudentT("y", nu=nu, mu=mu, sigma=sigma, observed=y, dims="obs")
        else:
            pm.Normal("y", mu=mu, sigma=sigma, observed=y, dims="obs")
    return model


def model_spec():
    """Which terms/likelihood M1-M5 use; M5 is fixed once 04_sampling has run."""
    spec = {k: {"terms": v, "likelihood": "normal", "formula": MODEL_FORMULA[k]}
            for k, v in MODEL_TERMS.items()}
    res = read_results()
    if "m5_base" in res:
        base = res["m5_base"]
        spec["M5"] = {"terms": MODEL_TERMS[base], "likelihood": "student",
                      "formula": MODEL_FORMULA[base] + " (Student-t)", "base": base}
    return spec


def load_idata(name):
    import arviz as az

    return az.from_netcdf(IDATA / f"idata_{name}.nc")


# ---------------------------------------------------------------- results store

def read_results():
    return json.loads(RESULTS.read_text()) if RESULTS.exists() else {}


def save_results(**kw):
    res = read_results()
    res.update(kw)
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float))
