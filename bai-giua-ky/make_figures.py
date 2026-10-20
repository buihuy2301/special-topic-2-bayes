"""Simulated figures for the midterm essay: how the training sample shapes the
posterior of a Bayesian linear regression.

Each figure isolates one property of the sample (size, noise, spread of x,
range covered, collinearity, outliers) or the prior-vs-data balance. All use the
closed-form conjugate posterior with known sigma, except the outlier figure,
which uses a grid over (intercept, slope).

Usage (from the repository root): .venv/bin/python bai-giua-ky/make_figures.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

SEED = 2026
OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREY, GREEN, ORANGE = "#2471a3", "#c0392b", "#7f8c8d", "#27ae60", "#e67e22"

BETA_TRUE = np.array([1.0, 2.0])  # intercept, slope
SIGMA = 1.0


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png")
    plt.close(fig)
    print("saved", OUT / f"{name}.png")


def simulate(n, rng, sigma=SIGMA, x_sd=1.0, x_center=0.0):
    x = x_center + x_sd * rng.standard_normal(n)
    y = BETA_TRUE[0] + BETA_TRUE[1] * x + sigma * rng.standard_normal(n)
    return np.column_stack([np.ones(n), x]), y


def posterior(X, y, sigma=SIGMA, m0=None, tau=2.0):
    """Conjugate posterior N(m_n, V_n) for beta with known sigma and prior N(m0, tau² I)."""
    p = X.shape[1]
    m0 = np.zeros(p) if m0 is None else m0
    V0_inv = np.eye(p) / tau**2
    Vn = np.linalg.inv(V0_inv + X.T @ X / sigma**2)
    mn = Vn @ (V0_inv @ m0 + X.T @ y / sigma**2)
    return mn, Vn


# ---------------------------------------------------------------------------
# 1. Sequential learning: the posterior of the slope narrows as n grows.
# ---------------------------------------------------------------------------
def fig_sequential():
    rng = np.random.default_rng(SEED)
    X, y = simulate(500, rng)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    grid = np.linspace(-3, 5, 800)
    colors = plt.cm.viridis(np.linspace(0, .9, 5))
    for n, c in zip([0, 2, 10, 50, 250], colors):
        mn, Vn = posterior(X[:n], y[:n]) if n else (np.zeros(2), np.eye(2) * 4.0)
        label = "tiên nghiệm (n = 0)" if n == 0 else f"n = {n}"
        axes[0].plot(grid, stats.norm.pdf(grid, mn[1], np.sqrt(Vn[1, 1])), color=c, lw=2, label=label)
    axes[0].axvline(BETA_TRUE[1], color=RED, ls="--", lw=1, label="giá trị thật β₁ = 2")
    axes[0].set(xlabel="β₁ (hệ số góc)", ylabel="mật độ hậu nghiệm", xlim=(-3, 5))
    axes[0].set_title("Hậu nghiệm của β₁ khi n tăng")
    axes[0].legend(fontsize=8)

    ns = np.unique(np.geomspace(1, 500, 60).astype(int))
    stats_n = np.array([[*posterior(X[:n], y[:n])[0], np.sqrt(posterior(X[:n], y[:n])[1][1, 1])] for n in ns])
    mean, sd = stats_n[:, 1], stats_n[:, 2]
    axes[1].fill_between(ns, mean - 1.96 * sd, mean + 1.96 * sd, color=BLUE, alpha=.25, label="khoảng tin cậy hậu nghiệm 95%")
    axes[1].plot(ns, mean, color=BLUE, label="trung bình hậu nghiệm")
    axes[1].axhline(BETA_TRUE[1], color=RED, ls="--", lw=1)
    axes[1].set(xscale="log", xlabel="cỡ mẫu n (thang logarit)", ylabel="β₁")
    axes[1].set_title("Trung bình và khoảng 95% theo n")
    axes[1].legend(fontsize=8)
    save(fig, "fig_sequential")


# ---------------------------------------------------------------------------
# 2. Prior strength versus sample size: shrinkage towards the prior mean.
# ---------------------------------------------------------------------------
def fig_prior_vs_data():
    rng = np.random.default_rng(SEED + 1)
    X, y = simulate(1000, rng)
    ns = np.unique(np.geomspace(2, 1000, 60).astype(int))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for tau, c in zip([0.05, 0.2, 1.0, 100.0], [RED, ORANGE, GREEN, BLUE]):
        means = [posterior(X[:n], y[:n], tau=tau)[0][1] for n in ns]
        axes[0].plot(ns, means, color=c, lw=2, label=f"τ = {tau:g}")
    axes[0].axhline(BETA_TRUE[1], color="k", ls="--", lw=1)
    axes[0].axhline(0, color=GREY, ls=":", lw=1)
    axes[0].set(xscale="log", xlabel="cỡ mẫu n (thang logarit)", ylabel="trung bình hậu nghiệm của β₁")
    axes[0].set_title("Ảnh hưởng của mức độ tập trung của tiên nghiệm")
    axes[0].legend(fontsize=8, title="độ lệch chuẩn tiên nghiệm")

    # Weight of the data in the posterior mean, w = data precision / total precision,
    # for x with unit variance: n / (n + sigma² / tau²).
    for tau, c in zip([0.05, 0.2, 1.0, 100.0], [RED, ORANGE, GREEN, BLUE]):
        w = ns / (ns + SIGMA**2 / tau**2)
        axes[1].plot(ns, w, color=c, lw=2, label=f"τ = {tau:g}")
    axes[1].set(xscale="log", xlabel="cỡ mẫu n (thang logarit)", ylabel="trọng số của dữ liệu w", ylim=(0, 1.02))
    axes[1].set_title("w = n / (n + σ²/τ²)")
    axes[1].legend(fontsize=8)
    save(fig, "fig_prior_vs_data")


# ---------------------------------------------------------------------------
# 3. Noise level and spread of x: posterior sd of the slope.
# ---------------------------------------------------------------------------
def fig_noise_spread():
    ns = np.geomspace(5, 1000, 100)
    tau = 2.0
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for sigma, c in zip([0.5, 1.0, 2.0], [GREEN, BLUE, RED]):
        sd = 1 / np.sqrt(ns * 1.0**2 / sigma**2 + 1 / tau**2)
        axes[0].plot(ns, sd, color=c, lw=2, label=f"σ = {sigma:g}")
    axes[0].set(xscale="log", yscale="log", xlabel="cỡ mẫu n", ylabel="độ lệch chuẩn hậu nghiệm của β₁")
    axes[0].set_title("Nhiễu σ lớn hơn → hậu nghiệm rộng hơn (s_x = 1)")
    axes[0].legend(fontsize=8)
    for x_sd, c in zip([0.25, 1.0, 4.0], [RED, BLUE, GREEN]):
        sd = 1 / np.sqrt(ns * x_sd**2 / SIGMA**2 + 1 / tau**2)
        axes[1].plot(ns, sd, color=c, lw=2, label=f"s_x = {x_sd:g}")
    axes[1].set(xscale="log", xlabel="cỡ mẫu n")
    axes[1].set_title("x phân tán hơn → hậu nghiệm hẹp hơn (σ = 1)")
    axes[1].legend(fontsize=8)
    save(fig, "fig_noise_spread")


# ---------------------------------------------------------------------------
# 4. Collinearity: joint posterior of two correlated slopes.
# ---------------------------------------------------------------------------
def fig_collinearity():
    rng = np.random.default_rng(SEED + 2)
    n, beta = 50, np.array([0.0, 1.0, 1.0])
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharex=True, sharey=True)
    t = np.linspace(0, 2 * np.pi, 200)
    for ax, rho in zip(axes, [0.0, 0.9, 0.99]):
        cov = np.array([[1, rho], [rho, 1]])
        x = rng.multivariate_normal([0, 0], cov, n)
        X = np.column_stack([np.ones(n), x])
        y = X @ beta + SIGMA * rng.standard_normal(n)
        mn, Vn = posterior(X, y)
        S = Vn[1:, 1:]
        # 95% ellipse of a bivariate normal: radius sqrt(chi2_2(0.95)).
        L = np.linalg.cholesky(S) * np.sqrt(stats.chi2.ppf(.95, 2))
        ell = mn[1:, None] + L @ np.vstack([np.cos(t), np.sin(t)])
        draws = rng.multivariate_normal(mn[1:], S, 400)
        ax.scatter(draws[:, 0], draws[:, 1], s=4, color=BLUE, alpha=.3)
        ax.plot(*ell, color=BLUE, lw=2)
        ax.plot(*beta[1:], "x", color=RED, ms=9, mew=2)
        r = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])
        ax.set_title(f"ρ(x₁, x₂) = {rho:g}\nsd(β₁) = {np.sqrt(S[0, 0]):.2f}, tương quan hậu nghiệm = {r:.2f}",
                     fontsize=10)
        ax.set(xlabel="β₁")
    axes[0].set(ylabel="β₂")
    save(fig, "fig_collinearity")


# ---------------------------------------------------------------------------
# 5. One outlier: Normal versus Student-t likelihood.
# ---------------------------------------------------------------------------
def fig_outlier():
    rng = np.random.default_rng(SEED + 3)
    n = 20
    x = np.sort(rng.uniform(0, 4, n))
    y = BETA_TRUE[0] + BETA_TRUE[1] * x + 0.6 * rng.standard_normal(n)
    y[-1] -= 9  # one gross error at the largest x
    sigma, nu = 0.6, 3
    b0 = np.linspace(-2, 5, 300)
    b1 = np.linspace(-1, 3.5, 300)
    B0, B1 = np.meshgrid(b0, b1, indexing="ij")
    mu = B0[..., None] + B1[..., None] * x
    prior = stats.norm.logpdf(B0, 0, 2) + stats.norm.logpdf(B1, 0, 2)
    logp = {"Chuẩn": stats.norm.logpdf(y, mu, sigma).sum(-1) + prior,
            "Student-t (ν = 3)": stats.t.logpdf(y, nu, mu, sigma).sum(-1) + prior}

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].scatter(x[:-1], y[:-1], color="k", s=18, zorder=3)
    axes[0].scatter(x[-1], y[-1], color=RED, s=40, zorder=3, label="ngoại lai")
    xs = np.linspace(0, 4, 50)
    axes[0].plot(xs, BETA_TRUE[0] + BETA_TRUE[1] * xs, color="k", ls="--", lw=1, label="đường hồi quy của mô hình sinh dữ liệu")
    for (name, lp), c in zip(logp.items(), [ORANGE, BLUE]):
        post = np.exp(lp - lp.max())
        post /= post.sum()
        m0, m1 = (post * B0).sum(), (post * B1).sum()
        axes[0].plot(xs, m0 + m1 * xs, color=c, lw=2, label=name)
        marg = post.sum(0) / (b1[1] - b1[0])
        axes[1].plot(b1, marg, color=c, lw=2, label=f"{name}: E[β₁] = {m1:.2f}")
    axes[0].set(xlabel="x", ylabel="y")
    axes[0].set_title("Đường hồi quy theo trung bình hậu nghiệm")
    axes[0].legend(fontsize=8)
    axes[1].axvline(BETA_TRUE[1], color="k", ls="--", lw=1)
    axes[1].set(xlabel="β₁", ylabel="mật độ hậu nghiệm")
    axes[1].set_title("Hậu nghiệm của hệ số góc")
    axes[1].legend(fontsize=8)
    save(fig, "fig_outlier")


# ---------------------------------------------------------------------------
# 6. Range covered by x: credible band of the mean vs predictive interval.
# ---------------------------------------------------------------------------
def fig_predictive():
    rng = np.random.default_rng(SEED + 4)
    n = 20
    x = rng.uniform(0, 1, n)
    X = np.column_stack([np.ones(n), x])
    y = X @ BETA_TRUE + SIGMA * rng.standard_normal(n)
    mn, Vn = posterior(X, y)
    xs = np.linspace(-0.5, 2.5, 200)
    Xs = np.column_stack([np.ones_like(xs), xs])
    mean = Xs @ mn
    sd_mu = np.sqrt(np.einsum("ij,jk,ik->i", Xs, Vn, Xs))
    sd_pred = np.sqrt(sd_mu**2 + SIGMA**2)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.axvspan(0, 1, color=GREY, alpha=.12, label="vùng có dữ liệu")
    ax.fill_between(xs, mean - 1.96 * sd_pred, mean + 1.96 * sd_pred, color=BLUE, alpha=.18,
                    label="khoảng dự đoán 95%")
    ax.fill_between(xs, mean - 1.96 * sd_mu, mean + 1.96 * sd_mu, color=BLUE, alpha=.45,
                    label="khoảng tin cậy hậu nghiệm 95% của E[y | x]")
    ax.plot(xs, mean, color=BLUE)
    ax.scatter(x, y, color="k", s=16, zorder=3)
    ax.set(xlabel="x", ylabel="y")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "fig_predictive")


if __name__ == "__main__":
    fig_sequential()
    fig_prior_vs_data()
    fig_noise_spread()
    fig_collinearity()
    fig_outlier()
    fig_predictive()
