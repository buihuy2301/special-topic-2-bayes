# %% [markdown]
# # 04_conjugate — Hậu nghiệm dạng đóng cho M1 (Normal–Inverse-Gamma), đối chiếu MCMC (mục 4.1)
# Owner: Nguyễn Thục Anh. Runs after 03_sampling (needs `idata_M1.nc`).
#
# Prior: beta | sigma² ~ N(m0, sigma² V0), sigma² ~ IG(a0, b0). Posterior:
#
# V_n = (V0⁻¹ + XᵀX)⁻¹,  m_n = V_n (V0⁻¹ m0 + Xᵀy),
# a_n = a0 + n/2,  b_n = b0 + ½ (yᵀy + m0ᵀV0⁻¹m0 − m_nᵀV_n⁻¹m_n)
#
# Marginally beta | y ~ multivariate t_{2a_n}(m_n, (b_n/a_n) V_n) and sigma² | y ~ IG(a_n, b_n).

# %%
from common import *  # noqa: F401,F403
import pymc as pm
from scipy import stats

d = load_clean()
sc = Scaler(d)
X = np.column_stack([np.ones(len(d)), sc.hp(d["hp"])])
y = sc.y(d["city"])
n, p = X.shape

m0, V0 = np.zeros(p), np.eye(p) * 2.5**2
a0, b0 = 2.0, 1.0  # E[sigma²] = 1 on the standardised scale

V0_inv = np.linalg.inv(V0)
Vn = np.linalg.inv(V0_inv + X.T @ X)
mn = Vn @ (V0_inv @ m0 + X.T @ y)
an = a0 + n / 2
bn = b0 + 0.5 * (y @ y + m0 @ V0_inv @ m0 - mn @ np.linalg.inv(Vn) @ mn)

beta_scale = np.sqrt(np.diag(bn / an * Vn))
df = 2 * an
closed = pd.DataFrame({
    "mean": mn, "sd": beta_scale * np.sqrt(df / (df - 2)),
    "ci_2.5%": mn + stats.t.ppf(.025, df) * beta_scale,
    "ci_97.5%": mn + stats.t.ppf(.975, df) * beta_scale,
}, index=["b0", "b_hp"])
sig2 = stats.invgamma(an, scale=bn)
print(f"a_n = {an:.1f}, b_n = {bn:.3f}, E[sigma | y] ≈ {np.sqrt(sig2.mean()):.3f}")
print(closed.round(4))

# %% [markdown]
# Check: the same NIG prior written in PyMC and sampled with NUTS must reproduce the
# closed form; a mismatch would mean a coding error.

# %%
with pm.Model():
    sigma2 = pm.InverseGamma("sigma2", a0, b0)
    beta = pm.MvNormal("beta", m0, cov=sigma2 * V0)
    pm.Normal("y", X @ beta, pm.math.sqrt(sigma2), observed=y)
    nig_idata = pm.sample(**{**SAMPLE_KW, "idata_kwargs": {}})

nig_post = nig_idata.posterior["beta"].values.reshape(-1, p)
mcmc_nig = pd.DataFrame({"mean": nig_post.mean(0), "sd": nig_post.std(0),
                         "ci_2.5%": np.quantile(nig_post, .025, 0),
                         "ci_97.5%": np.quantile(nig_post, .975, 0)}, index=["b0", "b_hp"])

m1 = load_idata("M1").posterior
m1_post = np.column_stack([m1["b0"].values.ravel(), m1["b"].sel(term="hp").values.ravel()])
mcmc_m1 = pd.DataFrame({"mean": m1_post.mean(0), "sd": m1_post.std(0),
                        "ci_2.5%": np.quantile(m1_post, .025, 0),
                        "ci_97.5%": np.quantile(m1_post, .975, 0)}, index=["b0", "b_hp"])

cmp = pd.concat({"closed form (NIG)": closed, "NUTS, NIG prior": mcmc_nig,
                 "NUTS, M1 weak prior": mcmc_m1})
cmp.to_csv(TAB / "tab_4_1_conjugate_vs_mcmc.csv")
print(cmp.round(4).to_string())

max_diff = float(np.abs(closed["mean"] - mcmc_nig["mean"]).max())
assert max_diff < 0.01, f"closed form and MCMC disagree by {max_diff:.4f}"

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
for j, (ax, label) in enumerate(zip(axes, ["β0 (hệ số chặn)", "β_HP"])):
    grid = np.linspace(mn[j] - 4.5 * beta_scale[j], mn[j] + 4.5 * beta_scale[j], 300)
    ax.plot(grid, stats.t.pdf(grid, df, mn[j], beta_scale[j]), c="k", lw=2, label="dạng đóng (t)")
    ax.hist(nig_post[:, j], bins=60, density=True, alpha=.4, color="#2471a3", label="NUTS, prior NIG")
    ax.hist(m1_post[:, j], bins=60, density=True, histtype="step", color="#c0392b", label="NUTS, M1")
    ax.set(title=label, xlabel="thang chuẩn hoá")
axes[0].legend(fontsize=8)
fig.suptitle("Hình 4.1 — Hậu nghiệm dạng đóng và MCMC cho M1")
savefig(fig, "fig_4_1_conjugate.png")

save_results(conjugate={"a_n": an, "b_n": float(bn), "m_n": mn.tolist(),
                        "max_abs_mean_diff_vs_nuts": max_diff})
