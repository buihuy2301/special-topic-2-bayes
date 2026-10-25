# %% [markdown]
# # 05_evaluation — PPC, so sánh mô hình, trả lời Q1–Q4 (Chương 5)
# Owner: Nguyễn Hồng Phúc. Runs after 03_sampling.

# %%
from common import *  # noqa: F401,F403
import arviz as az
from scipy import stats

d = load_clean()
sc = Scaler(d)
spec = model_spec()
idatas = {name: load_idata(name) for name in spec}


def draws(idata, terms):
    post = idata.posterior.stack(sample=("chain", "draw"))
    b = post["b"].sel(term=terms).values  # (terms, S)
    nu = post["nu"].values if "nu" in post else None
    return post["b0"].values, b, post["sigma"].values, nu


def predict_mpg(name, hp, weight, usa, kind="pred", seed=SEED):
    """Posterior draws (S, n) in MPG of exp(mu) ('mu') or a new observation ('pred').

    The response is log(City), so exp(mu) is the conditional *median* of City, not its mean;
    under the Student-t likelihood the mean of City does not even exist.
    """
    s = spec[name]
    b0, b, sigma, nu = draws(idatas[name], s["terms"])
    X = design(None, sc, s["terms"], hp=hp, weight=weight, usa=usa)
    mu = b0[:, None] + (X @ b).T
    if kind == "mu":
        return sc.to_mpg(mu)
    rng = np.random.default_rng(seed)
    eps = rng.standard_normal(mu.shape) if nu is None else rng.standard_t(nu[:, None], mu.shape)
    return sc.to_mpg(mu + sigma[:, None] * eps)


def hdi(x, prob=.95):
    return az.hdi(np.asarray(x), hdi_prob=prob)


# %% [markdown]
# ## 5.1 Posterior predictive check (thang MPG)

# %%
fig, axes = plt.subplots(2, 3, figsize=(12, 6.5), sharex=True, sharey=True)
grid = np.linspace(10, 55, 300)
rng = np.random.default_rng(SEED)
for ax, name in zip(axes.ravel(), spec):
    rep = sc.to_mpg(idatas[name].posterior_predictive["y"].stack(s=("chain", "draw")).values.T)
    for i in rng.choice(len(rep), 100, replace=False):
        ax.plot(grid, stats.gaussian_kde(rep[i])(grid), c="#2471a3", alpha=.08, lw=.8)
    ax.plot(grid, stats.gaussian_kde(d["city"])(grid), c="k", lw=2)
    ax.set_title(f"{name}: {spec[name]['formula']}", fontsize=9)
axes.ravel()[-1].axis("off")
for ax in axes[-1]:
    ax.set_xlabel("City (MPG)")
fig.suptitle("Hình 5.1 — Posterior predictive check: dữ liệu thật (đen) và 100 bộ tái tạo (xanh)")
savefig(fig, "fig_5_1_ppc.png")

# Bayesian p-values for a few statistics (near 0 or 1 = the model misses that feature).
ppp_rows = []
for name in spec:
    rep = sc.to_mpg(idatas[name].posterior_predictive["y"].stack(s=("chain", "draw")).values.T)
    for stat, f in [("mean", np.mean), ("sd", np.std), ("max", np.max), ("min", np.min)]:
        ppp_rows.append({"model": name, "stat": stat, "observed": f(d["city"]),
                         "p_value": np.mean(f(rep, axis=1) >= f(d["city"]))})
ppp = pd.DataFrame(ppp_rows).pivot(index="model", columns="stat", values="p_value")
ppp.to_csv(TAB / "tab_5_1_ppc_pvalues.csv")
print(ppp.round(3))

# %% [markdown]
# ## 5.2 So sánh mô hình: PSIS-LOO (ELPD) và WAIC

# %%
cmp_loo = az.compare(idatas, ic="loo")
cmp_waic = az.compare(idatas, ic="waic")
cmp_loo.to_csv(TAB / "tab_5_2_compare_loo.csv")
cmp_waic.to_csv(TAB / "tab_5_2_compare_waic.csv")
print(cmp_loo[["rank", "elpd_loo", "p_loo", "elpd_diff", "se", "dse", "weight"]].round(2))
print(cmp_waic[["rank", "elpd_waic", "p_waic", "elpd_diff", "se", "dse"]].round(2))

pareto = {}
for name, idata in idatas.items():
    k = az.loo(idata, pointwise=True).pareto_k.values
    pareto[name] = {"k_gt_0.7": int((k > .7).sum()), "k_gt_0.5": int((k > .5).sum()), "max_k": float(k.max())}
print(pd.DataFrame(pareto).T)

fig, ax = plt.subplots(figsize=(7, 3.5))
az.plot_compare(cmp_loo, ax=ax, insample_dev=False)
ax.set_title("Hình 5.2 — So sánh mô hình bằng PSIS-LOO")
savefig(fig, "fig_5_2_compare.png")

FINAL = cmp_loo.index[0]
# The top-ranked model is final; flag it when the runner-up is within 2 dSE.
runner_up = cmp_loo.index[1]
gap, dse = cmp_loo.loc[runner_up, "elpd_diff"], cmp_loo.loc[runner_up, "dse"]
note = f"rank 1 by PSIS-LOO; {runner_up} is {gap:.2f} ELPD behind (dse {dse:.2f}, {gap / dse:.1f} SE)"
print("Final model:", FINAL, "-", note)

# %% [markdown]
# ## 5.3 Q1 — Quan hệ giữa các biến: diễn giải β_HP
# On the log scale, +10 hp multiplies City by exp(10 · β_HP · sd_logy / sd_hp).

# %%
def pct_per_10hp(name):
    b_hp = idatas[name].posterior["b"].sel(term="hp").values.ravel()
    return 100 * (np.exp(10 * b_hp * sc.y_sd / sc.hp_sd) - 1)


q1 = {}
for name in ["M1", FINAL]:
    pct = pct_per_10hp(name)
    lo, hi = hdi(pct)
    q1[name] = {"pct_per_10hp_mean": pct.mean(), "hdi_low": lo, "hdi_high": hi,
                "p_negative": float(np.mean(pct < 0))}
    print(f"{name}: +10 hp -> City {pct.mean():+.2f}% (HDI 95% {lo:+.2f}%, {hi:+.2f}%)")

# Absolute effect for a median car (140 -> 150 hp), from M1 (HP only).
mu140, mu150 = (predict_mpg("M1", hp, None, 0, kind="mu")[:, 0] for hp in (140, 150))
diff = mu150 - mu140
q1["M1_mpg_140_to_150"] = {"mean": diff.mean(), "hdi": hdi(diff).tolist()}
print(f"M1: 140 -> 150 hp changes City by {diff.mean():+.2f} MPG (HDI {hdi(diff).round(2)})")

if "weight" in spec[FINAL]["terms"]:
    b_w = idatas[FINAL].posterior["b"].sel(term="weight").values.ravel()
    pct_100kg = 100 * (np.exp(100 * b_w * sc.y_sd / sc.w_sd) - 1)
    q1["weight_pct_per_100kg"] = {"mean": pct_100kg.mean(), "hdi": hdi(pct_100kg).tolist()}
    print(f"{FINAL}: +100 kg -> City {pct_100kg.mean():+.2f}% (HDI {hdi(pct_100kg).round(2)})")

# %%
fig, ax = plt.subplots(figsize=(7, 4.5))
hp_grid = np.linspace(50, 310, 120)
mu = predict_mpg("M1", hp_grid, None, 0, kind="mu")
pred = predict_mpg("M1", hp_grid, None, 0, kind="pred")
ax.fill_between(hp_grid, *np.quantile(pred, [.025, .975], axis=0), color="#aed6f1", alpha=.5,
                label="khoảng dự đoán 95%")
band = np.array([hdi(mu[:, i]) for i in range(len(hp_grid))])
ax.fill_between(hp_grid, band[:, 0], band[:, 1], color="#2471a3", alpha=.5, label="HDI 95% của trung vị")
ax.plot(hp_grid, np.median(mu, 0), c="#1b4f72")
for o, sub in d.groupby("origin"):
    ax.scatter(sub["hp"], sub["city"], s=16, c=COLOR[o], label=o, zorder=3)
ax.set(xlabel="Horsepower (hp)", ylabel="City (MPG)", title="Hình 5.3 — M1: City theo HP")
ax.legend(fontsize=8)
savefig(fig, "fig_5_3_q1_m1_fit.png")

# %% [markdown]
# ## 5.4 Q2 — Xe Mỹ và xe nước ngoài

# %%
q2 = {}
for name in ["M2", "M3", FINAL]:
    post = idatas[name].posterior["b"]
    b_usa = post.sel(term="usa").values.ravel()
    entry = {"b_usa_mean": b_usa.mean(), "b_usa_hdi": hdi(b_usa).tolist(),
             "p_b_usa_gt_0": float(np.mean(b_usa > 0)),
             "pct_effect_usa": 100 * (np.exp(b_usa.mean() * sc.y_sd) - 1)}
    if "hp_usa" in spec[name]["terms"]:
        b_int = post.sel(term="hp_usa").values.ravel()
        entry.update(b_hp_usa_mean=b_int.mean(), b_hp_usa_hdi=hdi(b_int).tolist(),
                     p_b_hp_usa_gt_0=float(np.mean(b_int > 0)))
    q2[name] = entry
    print(name, {k: np.round(v, 3) for k, v in entry.items()})

# %%
panels = [("M3", None, "M3: HP × USA (đường riêng)")]
if "weight" in spec[FINAL]["terms"]:
    panels.append((FINAL, d["weight"].mean(), f"{FINAL}: Weight cố định ở trung bình"))
fig, axes = plt.subplots(1, len(panels), figsize=(6 * len(panels), 4.5), sharey=True, squeeze=False)
for ax, (name, w, title) in zip(axes[0], panels):
    for usa, o in [(1, "USA"), (0, "Nước ngoài")]:
        mu = predict_mpg(name, hp_grid, w, usa, kind="mu")
        band = np.array([hdi(mu[:, i]) for i in range(len(hp_grid))])
        ax.fill_between(hp_grid, band[:, 0], band[:, 1], color=COLOR[o], alpha=.25)
        ax.plot(hp_grid, np.median(mu, 0), c=COLOR[o], label=o)
        sub = d[d["usa"] == usa]
        ax.scatter(sub["hp"], sub["city"], s=14, c=COLOR[o], alpha=.7)
    ax.set(xlabel="Horsepower (hp)", ylabel="City (MPG)", title=title)
    ax.legend(fontsize=8)
fig.suptitle("Hình 5.4 — Đường hồi quy và HDI 95% cho xe Mỹ và xe nước ngoài")
savefig(fig, "fig_5_4_q2_usa.png")

# %% [markdown]
# ## 5.5 Q3 — Ngoại lai: phần dư chuẩn hoá, Pareto-k, Normal vs Student-t

# %%
normal_name = spec["M5"]["base"]  # the Normal model M5 robustifies
post = idatas[normal_name].posterior
mu_mean = post["mu"].mean(("chain", "draw")).values
resid_std = (sc.y(d["city"]) - mu_mean) / post["sigma"].mean().item()
k_vals = az.loo(idatas[normal_name], pointwise=True).pareto_k.values
k_vals_m5 = az.loo(idatas["M5"], pointwise=True).pareto_k.values
fitted_mpg = sc.to_mpg(mu_mean)

out = d[["name", "type", "origin", "hp", "weight", "engine_size", "city", "price_max"]].copy()
out["type"] = out["type"].map(TYPE_LABEL)
out["fitted_mpg"] = fitted_mpg.round(1)
out["std_resid"] = resid_std.round(2)
out[f"pareto_k_{normal_name}"] = k_vals.round(2)
out["pareto_k_M5"] = k_vals_m5.round(2)
CANDIDATES = ["Geo Metro", "Honda Civic", "Suzuki Swift", "Mazda RX-7", "Mercedes-Benz 300E"]
flag = (np.abs(resid_std) > 2) | (k_vals > .5) | out["name"].isin(CANDIDATES) | (out["type"] == "Van")
outliers = out[flag].sort_values("std_resid")
outliers.to_csv(TAB / "tab_5_5_outliers.csv", index=False)
print(outliers.to_string(index=False))

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
ax = axes[0]
for o in COLOR:
    m = out["origin"] == o
    ax.scatter(out.loc[m, "fitted_mpg"], resid_std[m], s=16, c=COLOR[o], label=o)
ax.axhline(0, c="k", lw=.8)
for yv in (-2, 2):
    ax.axhline(yv, c="grey", ls="--", lw=.8)
for i in np.where((np.abs(resid_std) > 2) | out["name"].isin(CANDIDATES))[0]:
    ax.annotate(out["name"].iat[i], (out["fitted_mpg"].iat[i], resid_std[i]), fontsize=7,
                xytext=(3, 2), textcoords="offset points")
ax.set(xlabel=f"City dự đoán bởi {normal_name} (MPG)", ylabel="Phần dư chuẩn hoá",
       title=f"Phần dư chuẩn hoá — {normal_name}")
ax.legend(fontsize=8)
ax = axes[1]
ax.scatter(np.arange(len(d)), k_vals, s=14, c="#2471a3", label=f"{normal_name} (Normal)")
ax.scatter(np.arange(len(d)), k_vals_m5, s=14, c="#e67e22", marker="x", label="M5 (Student-t)")
for yv in (.5, .7):
    ax.axhline(yv, c="grey", ls="--", lw=.8)
for i in np.argsort(k_vals)[-5:]:
    ax.annotate(out["name"].iat[i], (i, k_vals[i]), fontsize=7, xytext=(3, 2), textcoords="offset points")
ax.set(xlabel="Chỉ số quan sát", ylabel="Pareto k", title="Pareto-k của PSIS-LOO")
ax.legend(fontsize=8)
fig.suptitle("Hình 5.5 — Các điểm ngoại lai")
savefig(fig, "fig_5_5_q3_outliers.png")

# %%
coef_shift = pd.concat({
    normal_name: az.summary(idatas[normal_name], var_names=["b0", "b", "sigma"], hdi_prob=.95),
    "M5": az.summary(idatas["M5"], var_names=["b0", "b", "sigma", "nu"], hdi_prob=.95),
})[["mean", "sd", "hdi_2.5%", "hdi_97.5%"]]
coef_shift.to_csv(TAB / "tab_5_5_normal_vs_student.csv")
print(coef_shift.round(3).to_string())

# %% [markdown]
# ## 5.6 Q4 — Dự đoán City cho xe 300 hp
# 300 hp is the sample maximum, so this sits on the edge of the data. For models with
# Weight, a generic 300 hp car gets the mean weight of the three real cars with ≥ 295 hp.

# %%
real = d[d["hp"] >= 295][["name", "hp", "weight", "usa", "city"]].reset_index(drop=True)
w300 = real["weight"].mean()
print(real.to_string(index=False), f"\nweight used for a generic 300 hp car: {w300:.0f} kg")

q4_rows = []
for name in dict.fromkeys(["M1", "M3", FINAL]):
    for usa, o in [(1, "USA"), (0, "Nước ngoài")]:
        pred = predict_mpg(name, 300, w300, usa)[:, 0]
        mu = predict_mpg(name, 300, w300, usa, kind="mu")[:, 0]
        lo, hi = np.quantile(pred, [.025, .975])
        q4_rows.append({"model": name, "origin": o, "median_city": mu.mean(),
                        "median_hdi": hdi(mu).round(2).tolist(),
                        "pred_median": np.median(pred), "pi95_low": lo, "pi95_high": hi})
q4 = pd.DataFrame(q4_rows)
q4.to_csv(TAB / "tab_5_6_q4_300hp.csv", index=False)
print(q4.round(2).to_string(index=False))

# Each real car predicted from its own covariates with the final model.
rows = []
for _, r in real.iterrows():
    pred = predict_mpg(FINAL, r["hp"], r["weight"], r["usa"])[:, 0]
    lo, hi = np.quantile(pred, [.025, .975])
    rows.append({**r.to_dict(), "pred_median": np.median(pred), "pi95_low": lo, "pi95_high": hi,
                 "inside_pi95": bool(lo <= r["city"] <= hi)})
real_pred = pd.DataFrame(rows)
real_pred.to_csv(TAB / "tab_5_6_q4_real_cars.csv", index=False)
print(real_pred.round(2).to_string(index=False))

# %%
fig, ax = plt.subplots(figsize=(7, 4))
bins = np.linspace(8, 30, 70)
for name, c in zip(dict.fromkeys(["M1", FINAL]), ["#7f8c8d", "#2471a3"]):
    ax.hist(predict_mpg(name, 300, w300, 1)[:, 0], bins=bins, density=True, histtype="step", lw=2,
            color=c, label=f"{name} ({spec[name]['formula']})")
for _, r in real.iterrows():
    ax.axvline(r["city"], c="#c0392b", lw=1)
    ax.text(r["city"], ax.get_ylim()[1] * .95, r["name"], rotation=90, va="top", ha="right", fontsize=7)
ax.set(xlabel="City (MPG)", ylabel="Mật độ",
       title="Hình 5.6 — Phân phối dự đoán hậu nghiệm cho xe Mỹ 300 hp")
ax.legend(fontsize=8, loc="center right")
savefig(fig, "fig_5_6_q4_300hp.png")

# %%
save_results(final_model=FINAL, final_note=note,
             compare_loo=cmp_loo[["rank", "elpd_loo", "p_loo", "elpd_diff", "se", "dse", "weight"]].round(3).to_dict("index"),
             compare_waic=cmp_waic[["rank", "elpd_waic", "p_waic", "elpd_diff", "se", "dse"]].round(3).to_dict("index"),
             pareto_k=pareto, ppc_pvalues=ppp.round(3).to_dict("index"),
             q1=q1, q2=q2, q4=q4.round(3).to_dict("records"), q4_real=real_pred.round(3).to_dict("records"),
             q4_weight_kg=w300,
             q3_outliers=outliers[["name", "city", "fitted_mpg", "std_resid", f"pareto_k_{normal_name}"]].to_dict("records"))
print("saved", RESULTS)
