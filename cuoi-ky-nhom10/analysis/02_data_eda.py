# %% [markdown]
# # 02_data_eda — Làm sạch dữ liệu, thống kê mô tả, EDA (Chương 2)
# Owner: TV2. Output: `outputs/data_clean.csv` (used by every later module),
# section 2.5 statistics, figures 2.6, VIF, and an OLS baseline (section 3.1).

# %%
from common import *  # noqa: F401,F403  (paths, Scaler, savefig, ...)
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# %% [markdown]
# ## 2.3 Làm sạch dữ liệu
# `*` → NA; RPM columns stored as text with thousands separators ("6,300") → numbers.

# %%
raw = pd.read_csv(RAW_CSV, na_values="*", thousands=",")
d = raw.rename(columns=RENAME)
assert len(d) == 93 and list(d.columns) == list(RENAME.values())

missing = d.isna().sum()
missing = missing[missing > 0]
missing_rows = {col: d.loc[d[col].isna(), "name"].tolist() for col in missing.index}
print(missing.to_string())
for col, names in missing_rows.items():
    print(f"{col}: {names}")

# The model variables have no missing values, so no row is dropped.
MODEL_VARS = ["city", "hp", "weight", "usa"]
assert d[MODEL_VARS].notna().all().all()
d.to_csv(CLEAN_CSV, index=False)
print("saved", CLEAN_CSV)

# %% [markdown]
# ## 2.4 Đơn vị nhiên liệu
# The header says km/100L and the PDF says litres/100km, but values run 15–46 and
# Geo Metro (the most frugal car) has 46, so the column behaves like miles per
# gallon (higher = more efficient). The report assumes **MPG**;
# L/100km = 235.2 / MPG if needed.

# %%
geo = d.loc[d["name"].str.contains("Geo Metro"), ["name", "city", "hp", "weight"]]
print(geo.to_string(index=False))

# %% [markdown]
# ## 2.5 Thống kê mô tả

# %%
d = load_clean()
desc = d[["city", "open_road", "hp", "weight", "engine_size", "price"]].describe().T
desc.to_csv(TAB / "tab_2_5_describe.csv")
print(desc.round(2).to_string())

by_origin = d.groupby("origin")[["city", "hp", "weight", "engine_size", "price"]].agg(["mean", "median"])
by_origin.to_csv(TAB / "tab_2_5_by_origin.csv")
print(by_origin.round(1).to_string())

stats_25 = {
    "n": len(d), "n_usa": int(d["usa"].sum()), "n_foreign": int((d["usa"] == 0).sum()),
    "hp_min": int(d["hp"].min()), "hp_max": int(d["hp"].max()), "hp_median": float(d["hp"].median()),
    "city_min": int(d["city"].min()), "city_max": int(d["city"].max()),
    "city_median": float(d["city"].median()),
    "corr_hp_city": round(d["hp"].corr(d["city"]), 3),
    "corr_city_open_road": round(d["city"].corr(d["open_road"]), 3),
    "missing": {k: v for k, v in missing_rows.items()},
}
save_results(data=stats_25)
print(stats_25)

# %% [markdown]
# ## 2.6 EDA — ma trận scatterplot, boxplot theo Type

# %%
cols = {"city": "City (MPG)", "open_road": "Open Road (MPG)", "hp": "HP",
        "weight": "Weight (kg)", "engine_size": "Engine (L)", "price": "Price ($1000)"}
g = sns.pairplot(d.rename(columns=cols), vars=list(cols.values()), hue="origin",
                 palette=COLOR, corner=True, plot_kws={"s": 18, "alpha": .75},
                 diag_kws={"common_norm": False})
g.figure.suptitle("Hình 2.6a — Ma trận scatterplot theo xuất xứ", y=1.01)
savefig(g.figure, "fig_2_6_scatter.png")

corr = d[list(cols)].rename(columns=cols).corr()
corr.to_csv(TAB / "tab_2_6_corr.csv")
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, ax=ax)
ax.set_title("Hình 2.6b — Ma trận tương quan")
savefig(fig, "fig_2_6_corr.png")

# %%
d["type_label"] = d["type"].map(TYPE_LABEL)
order = d.groupby("type_label")["city"].median().sort_values().index
fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(d, x="type_label", y="city", order=order, color="#d5d8dc", ax=ax, showfliers=False)
sns.stripplot(d, x="type_label", y="city", order=order, hue="origin", palette=COLOR,
              ax=ax, size=4, jitter=.2)
ax.set(xlabel="Type", ylabel="City (MPG)", title="Hình 2.6c — City theo loại xe")
savefig(fig, "fig_2_6_box_type.png")

# %% [markdown]
# Preliminary outlier flags: cars far from the HP–City trend
# (OLS log(City) ~ HP, |studentised residual| > 2).

# %%
fig, ax = plt.subplots(figsize=(7, 5))
for o, sub in d.groupby("origin"):
    ax.scatter(sub["hp"], sub["city"], s=20, c=COLOR[o], label=o, alpha=.8)
ols_eda = sm.OLS(np.log(d["city"]), sm.add_constant(d["hp"])).fit()
stud = ols_eda.get_influence().resid_studentized_external
flag = d.loc[np.abs(stud) > 2, ["name", "hp", "city"]]
for _, r in flag.iterrows():
    ax.annotate(r["name"], (r["hp"], r["city"]), fontsize=7, xytext=(4, 2), textcoords="offset points")
ax.set(xlabel="Horsepower (hp)", ylabel="City (MPG)", title="Hình 2.6d — HP và City, các điểm lạ sơ bộ")
ax.legend()
savefig(fig, "fig_2_6_hp_city_flags.png")
print(flag.assign(stud_resid=stud[np.abs(stud) > 2].round(2)).to_string(index=False))

# %% [markdown]
# ## 3.2–3.3 Đa cộng tuyến (VIF), City vs log(City), OLS baseline

# %%
X = d[["hp", "weight", "engine_size"]]
vif = pd.Series([variance_inflation_factor(sm.add_constant(X).values, i + 1) for i in range(X.shape[1])],
                index=X.columns, name="VIF")
X2 = d[["hp", "weight", "usa"]]
vif_m4 = pd.Series([variance_inflation_factor(sm.add_constant(X2).values, i + 1) for i in range(X2.shape[1])],
                   index=X2.columns, name="VIF (M4)")
vif_tab = pd.concat([vif, vif_m4], axis=1)
vif_tab.to_csv(TAB / "tab_3_2_vif.csv")
print(vif_tab.round(2).to_string())

# %%
# Compare response scales on the City scale (log-likelihood includes the Jacobian).
rows = []
for label, yy, jac in [("City", d["city"], 0.0),
                       ("log(City)", np.log(d["city"]), -np.log(d["city"]).sum())]:
    m = sm.OLS(yy, sm.add_constant(d["hp"])).fit()
    rows.append({"response": label, "R2": m.rsquared, "loglik_city_scale": m.llf + jac,
                 "AIC_city_scale": -2 * (m.llf + jac) + 2 * 3})
resp_tab = pd.DataFrame(rows)
resp_tab.to_csv(TAB / "tab_3_3_response_scale.csv", index=False)
print(resp_tab.round(3).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, (label, yy) in zip(axes, [("City", d["city"]), ("log(City)", np.log(d["city"]))]):
    m = sm.OLS(yy, sm.add_constant(d["hp"])).fit()
    ax.scatter(m.fittedvalues, m.resid, s=14, alpha=.7)
    ax.axhline(0, c="k", lw=.8)
    sm_lowess = sm.nonparametric.lowess(m.resid, m.fittedvalues)
    ax.plot(sm_lowess[:, 0], sm_lowess[:, 1], c="#e67e22")
    ax.set(title=f"Phần dư OLS: {label} ~ HP", xlabel="Giá trị khớp", ylabel="Phần dư")
fig.suptitle("Hình 3.3 — So sánh City và log(City)")
savefig(fig, "fig_3_3_response_scale.png")

# %%
# OLS baseline for every candidate model, on the same standardised scale as the Bayesian models.
sc = Scaler(d)
ols_rows = []
for name, terms in MODEL_TERMS.items():
    Xm = sm.add_constant(design(d, sc, terms))
    m = sm.OLS(sc.y(d["city"]), Xm).fit()
    ci = m.conf_int()
    for i, t in enumerate(["b0"] + terms):
        ols_rows.append({"model": name, "term": t, "coef": m.params[i], "se": m.bse[i],
                         "ci_low": ci[i, 0], "ci_high": ci[i, 1]})
ols_tab = pd.DataFrame(ols_rows)
ols_tab.to_csv(TAB / "tab_3_1_ols.csv", index=False)
print(ols_tab.round(3).to_string(index=False))

save_results(scaler={"hp_mu": sc.hp_mu, "hp_sd": sc.hp_sd, "w_mu": sc.w_mu, "w_sd": sc.w_sd,
                     "logy_mu": sc.y_mu, "logy_sd": sc.y_sd},
             vif=vif_tab.round(3).to_dict(),
             response_scale=resp_tab.round(3).to_dict("records"))
