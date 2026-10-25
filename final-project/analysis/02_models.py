# %% [markdown]
# # 02_models — Đặc tả M1–M5, prior predictive check, phân tích độ nhạy (Chương 3)
# Owner: Nguyễn Thị Bích Ngọc. Models are defined in `common.build_model`; response = standardised
# log(City), predictors HP and Weight standardised, USA kept as 0/1.
#
# M3 (full spec, section 3.5), on the standardised scale:
#
# y_i ~ N(mu_i, sigma^2),  mu_i = b0 + b1 HP_i + b2 USA_i + b3 HP_i USA_i,
# b_j ~ N(0, 2.5^2),  sigma ~ Half-Normal(1)

# %%
from common import *  # noqa: F401,F403
import arviz as az
import pymc as pm

d = load_clean()
sc = Scaler(d)
for name, terms in MODEL_TERMS.items():
    print(name, MODEL_FORMULA[name], "->", terms)

# %% [markdown]
# ## 3.6 Prior predictive check
# Data simulated from the prior should stay in a plausible range: City > 0 (always true on
# the log scale) and City ≤ 80 MPG. Checked for M3 under the three prior sets.

# %%
ppc_rows, prior_draws = [], {}
for prior in PRIOR_SD:
    with build_model(d, sc, MODEL_TERMS["M3"], prior=prior):
        pp = pm.sample_prior_predictive(draws=1000, random_seed=SEED)
    mpg = sc.to_mpg(pp.prior_predictive["y"].values.ravel())
    prior_draws[prior] = mpg
    ppc_rows.append({"prior": prior, "coef_sd": PRIOR_SD[prior],
                     "share_le_80mpg": np.mean(mpg <= 80),
                     "share_5_to_80mpg": np.mean((mpg >= 5) & (mpg <= 80)),
                     "median_mpg": np.median(mpg),
                     "q01": np.quantile(mpg, .01), "q99": np.quantile(mpg, .99)})
ppc_tab = pd.DataFrame(ppc_rows)
ppc_tab.to_csv(TAB / "tab_3_6_prior_predictive.csv", index=False)
print(ppc_tab.round(3).to_string(index=False))

# %%
fig, ax = plt.subplots(figsize=(7, 4))
bins = np.logspace(0, 3, 80)
for prior, c in zip(PRIOR_SD, ["#7f8c8d", "#2471a3", "#27ae60"]):
    ax.hist(np.clip(prior_draws[prior], 1, 1000), bins=bins, histtype="step", lw=1.5,
            density=True, color=c, label=f"{prior} (sd={PRIOR_SD[prior]})")
ax.hist(d["city"], bins=bins, color="k", alpha=.3, density=True, label="dữ liệu thật")
ax.axvline(80, ls="--", c="#c0392b", lw=1)
ax.set(xscale="log", xlabel="City mô phỏng từ prior (MPG, thang log, cắt ở 1–1000)",
       ylabel="Mật độ", title="Hình 3.6 — Prior predictive check cho M3")
ax.legend(fontsize=8)
savefig(fig, "fig_3_6_prior_predictive.png")

# %% [markdown]
# ## 3.7 Phân tích độ nhạy: M3 under flat / weak / tight priors

# %%
sens = {}
for prior in PRIOR_SD:
    with build_model(d, sc, MODEL_TERMS["M3"], prior=prior):
        sens[prior] = pm.sample(**SAMPLE_KW)
    sens[prior].to_netcdf(IDATA / f"idata_M3_prior_{prior}.nc")

rows = []
for prior, idata in sens.items():
    s = az.summary(idata, var_names=["b0", "b", "sigma"], hdi_prob=.95)
    s.insert(0, "prior", prior)
    rows.append(s)
sens_tab = pd.concat(rows)
sens_tab.to_csv(TAB / "tab_3_7_sensitivity.csv")
print(sens_tab[["prior", "mean", "sd", "hdi_2.5%", "hdi_97.5%", "r_hat"]].to_string())

# %%
fig, ax = plt.subplots(figsize=(7, 4))
az.plot_forest(list(sens.values()), model_names=list(sens), var_names=["b0", "b", "sigma"],
               combined=True, hdi_prob=.95, ax=ax)
ax.set_title("Hình 3.7 — Hậu nghiệm M3 dưới 3 bộ prior (HDI 95%)")
savefig(fig, "fig_3_7_sensitivity.png")

# Largest shift of a posterior mean relative to the weak prior, in posterior sds.
weak = sens_tab[sens_tab.prior == "weak"]
shift = {p: float((np.abs(sens_tab[sens_tab.prior == p]["mean"] - weak["mean"]) / weak["sd"]).max())
         for p in PRIOR_SD}
print("max |mean shift| / sd vs weak:", shift)
save_results(prior_predictive=ppc_tab.round(4).to_dict("records"), sensitivity_max_shift_sd=shift)
