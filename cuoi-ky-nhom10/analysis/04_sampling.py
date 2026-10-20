# %% [markdown]
# # 04_sampling — NUTS cho M1–M5, chẩn đoán hội tụ, Metropolis–Hastings tự cài (Chương 4)
# Owner: TV4. Output: `outputs/idata/idata_M*.nc`, posterior tables (4.4), diagnostics (4.3).

# %%
from common import *  # noqa: F401,F403
import arviz as az
import pymc as pm

d = load_clean()
sc = Scaler(d)
VARS = ["b0", "b", "sigma"]

# %% [markdown]
# ## 4.2 NUTS for M1–M4 (4 chains × 2000 draws, 1000 warm-up, seed 2026)

# %%
idatas = {}
for name, terms in MODEL_TERMS.items():
    with build_model(d, sc, terms):
        idatas[name] = pm.sample(**SAMPLE_KW)
        pm.sample_posterior_predictive(idatas[name], extend_inferencedata=True, random_seed=SEED,
                                       progressbar=False)
    idatas[name].to_netcdf(IDATA / f"idata_{name}.nc")

# %% [markdown]
# M5 = the best of M1–M4 by PSIS-LOO, refitted with a Student-t likelihood
# (robust to outliers). The full comparison is in 05_evaluation.

# %%
loo_rank = az.compare({k: idatas[k] for k in MODEL_TERMS}, ic="loo")
m5_base = loo_rank.index[0]
print(loo_rank[["rank", "elpd_loo", "se", "elpd_diff", "dse"]].round(2))
print("M5 base:", m5_base)
save_results(m5_base=m5_base)

with build_model(d, sc, MODEL_TERMS[m5_base], likelihood="student"):
    idatas["M5"] = pm.sample(**SAMPLE_KW)
    pm.sample_posterior_predictive(idatas["M5"], extend_inferencedata=True, random_seed=SEED,
                                   progressbar=False)
idatas["M5"].to_netcdf(IDATA / "idata_M5.nc")

# %% [markdown]
# ## 4.3 Chẩn đoán hội tụ: R-hat < 1.01, ESS bulk/tail > 400, 0 divergence

# %%
diag_rows = []
for name, idata in idatas.items():
    var_names = VARS + (["nu"] if name == "M5" else [])
    s = az.summary(idata, var_names=var_names)
    div = int(idata.sample_stats["diverging"].sum())
    diag_rows.append({"model": name, "max_r_hat": s["r_hat"].max(),
                      "min_ess_bulk": s["ess_bulk"].min(), "min_ess_tail": s["ess_tail"].min(),
                      "divergences": div,
                      "pass": bool(s["r_hat"].max() < 1.01 and s["ess_bulk"].min() > 400
                                   and s["ess_tail"].min() > 400 and div == 0)})
diag = pd.DataFrame(diag_rows)
diag.to_csv(TAB / "tab_4_3_diagnostics.csv", index=False)
print(diag.to_string(index=False))
assert diag["pass"].all(), "a chain failed the convergence gate — do not interpret coefficients"

# %%
for name, idata in idatas.items():
    var_names = VARS + (["nu"] if name == "M5" else [])
    axes = az.plot_trace(idata, var_names=var_names, compact=True, figsize=(10, 2 * len(var_names)))
    fig = axes.ravel()[0].figure
    fig.tight_layout()  # ArviZ subplot titles otherwise touch the tick labels
    fig.suptitle(f"Hình 4.3 — Trace plot {name}", y=1.01)
    savefig(fig, f"fig_4_3_trace_{name}.png")

    axes = az.plot_rank(idata, var_names=var_names, kind="vlines")
    fig = np.ravel(axes)[0].figure
    fig.tight_layout()  # ArviZ subplot titles otherwise touch the tick labels
    fig.suptitle(f"Hình 4.3 — Rank plot {name}", y=1.01)
    savefig(fig, f"fig_4_3_rank_{name}.png")

# %% [markdown]
# ## 4.4 Bảng tóm tắt hậu nghiệm (mean, sd, HDI 95%) và phân phối hậu nghiệm

# %%
rows = []
for name, idata in idatas.items():
    var_names = VARS + (["nu"] if name == "M5" else [])
    s = az.summary(idata, var_names=var_names, hdi_prob=.95)
    s.insert(0, "model", name)
    rows.append(s)
post = pd.concat(rows)
post.to_csv(TAB / "tab_4_4_posterior.csv")
print(post[["model", "mean", "sd", "hdi_2.5%", "hdi_97.5%", "ess_bulk", "r_hat"]].to_string())

# %%
fig, ax = plt.subplots(figsize=(7, 5))
az.plot_forest(list(idatas.values()), model_names=list(idatas), var_names=["b"],
               combined=True, hdi_prob=.95, ax=ax)
ax.axvline(0, c="k", lw=.8)
ax.set_title("Hình 4.4a — Hệ số hậu nghiệm M1–M5 (thang chuẩn hoá, HDI 95%)")
savefig(fig, "fig_4_4_forest.png")

for name in ["M3", m5_base]:
    axes = az.plot_posterior(idatas[name], var_names=VARS, hdi_prob=.95, ref_val=0)
    fig = np.ravel(axes)[0].figure
    fig.suptitle(f"Hình 4.4 — Phân phối hậu nghiệm {name}", y=1.02)
    savefig(fig, f"fig_4_4_posterior_{name}.png")

# %% [markdown]
# ## 4.2 (minh hoạ) Random-walk Metropolis–Hastings cho M1, viết tay
# Same priors as M1: b0, b1 ~ N(0, 2.5²), sigma ~ Half-Normal(1); sampled on (b0, b1, log sigma).

# %%
from scipy import stats

x = sc.hp(d["hp"])
y = sc.y(d["city"])


def log_post(theta):
    b0, b1, log_s = theta
    s = np.exp(log_s)
    return (stats.norm.logpdf(y, b0 + b1 * x, s).sum()
            + stats.norm.logpdf([b0, b1], 0, 2.5).sum()
            + stats.halfnorm.logpdf(s, scale=1) + log_s)  # + log|Jacobian| of sigma = exp(log_s)


def metropolis(n_iter, step, rng, start):
    chain = np.empty((n_iter, 3))
    cur, cur_lp, acc = np.array(start, float), log_post(start), 0
    for i in range(n_iter):
        prop = cur + step * rng.standard_normal(3)
        prop_lp = log_post(prop)
        if np.log(rng.uniform()) < prop_lp - cur_lp:
            cur, cur_lp, acc = prop, prop_lp, acc + 1
        chain[i] = cur
    return chain, acc / n_iter


rng = np.random.default_rng(SEED)
step = np.array([0.08, 0.08, 0.08])
chains, rates = [], []
for c in range(4):
    start = rng.normal(0, 1, 3)
    ch, rate = metropolis(6000, step, rng, start)
    chains.append(ch[1000:])  # 1000 burn-in
    rates.append(rate)
chains = np.stack(chains)
mh = az.from_dict(posterior={"b0": chains[..., 0], "b_hp": chains[..., 1],
                             "sigma": np.exp(chains[..., 2])})
mh_sum = az.summary(mh, hdi_prob=.95)
nuts_sum = az.summary(idatas["M1"], var_names=VARS, hdi_prob=.95)
nuts_sum.index = ["b0", "b_hp", "sigma"]
mh_cmp = pd.concat({"MH": mh_sum, "NUTS": nuts_sum})[["mean", "sd", "hdi_2.5%", "hdi_97.5%", "ess_bulk", "r_hat"]]
mh_cmp.to_csv(TAB / "tab_4_2_mh_vs_nuts.csv")
print("MH acceptance rates:", np.round(rates, 3))
print(mh_cmp.to_string())

axes = az.plot_trace(mh, compact=True, figsize=(10, 7.5))
fig = axes.ravel()[0].figure
fig.tight_layout()  # ArviZ subplot titles otherwise touch the tick labels
fig.suptitle("Hình 4.2 — Trace plot Metropolis–Hastings tự cài (M1)", y=1.01)
savefig(fig, "fig_4_2_mh_trace.png")

save_results(diagnostics=diag.to_dict("records"), mh_acceptance=[float(r) for r in rates],
             loo_rank_m1_m4=loo_rank["elpd_loo"].round(2).to_dict())
