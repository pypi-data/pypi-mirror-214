import numpy as np
from matplotlib import pylab as plt
import seaborn as sns
import scipy.stats as stats
from src import tarshim


def minmax(v):
    v = v - np.min(v)
    v = v / v.max()
    return v


def to_mean(v):
    return v - v.mean()


def do_stuff(normalization=None, method=None):
    x = np.linspace(-10, 10)
    y_obs = x * 1.12 + 3.12
    if normalization == "minmax":
        x = minmax(x)
        y_obs = minmax(y_obs)
    elif normalization == "to_mean":
        x = to_mean(x)
        y_obs = to_mean(y_obs)
    y_pred = y_obs + np.random.randn(len(x)) * 5.0
    if method == "SVM":
        y_pred = y_obs + 0.1 * (y_obs ** 2) + np.random.randn(len(x)) * 2.0
    if method == "RNN":
        y_pred = y_obs + np.random.randn(len(x)) * 5.0
        sel = np.random.rand(len(y_pred)) > 0.8
        y_pred[sel] = np.min(y_pred) - 3
    return y_obs, y_pred


def visualize(results):
    y_obs, y_pred = results
    fig = plt.figure(dpi=220, figsize=(4, 4))
    tarshim.plot_observed_vs_predicted(observations=y_obs, predictions=y_pred, fig=fig)
    return fig


def visualize0(results):
    y_obs, y_pred = results
    fig, axes = plt.subplots(dpi=220, figsize=(4, 4))
    ax = axes
    ax.plot(y_pred, y_obs, "o")
    ax.set_xlabel("Prediction")
    ax.set_ylabel("Observation")
    ax.grid(True)
    return fig


def visualize_with_diagnostics(results, metrics=False, title=None):
    fig = visualize(results)
    axes = fig.axes
    # for ax in axes:
    #     sns.despine(ax=ax, top=False, left=False, bottom=False, right=False)
    #     ax.grid(True)
    if metrics:
        ax = axes[0]
        y_obs, y_pred = results
        corr = stats.spearmanr(y_obs, y_pred)
        rho, p = corr.correlation, corr.pvalue
        n = len(y_obs)
        ax.text(
            0.02,
            1,
            f"$\\rho={rho:.3f} (p={p:.3e})$\n$(N={n})$",
            transform=ax.transAxes,
            va="top",
        )
    if title:
        fig.suptitle(title)
    return fig


for normalization in (
    "none",
    "minmax",
    "to_mean",
):
    for method in (
        "LR",
        "SVM",
        "RNN",
    ):
        results = do_stuff(normalization=normalization, method=method)
        # fig = visualize_with_diagnostics(
        #     results, metrics=True,
        #     title=f'{normalization} {method}.'
        # )
        if method == "LR" and normalization == "none":
            fig, ax = plt.subplots()
            y_obs, y_pred = results

            tarshim.plot_residuals(observations=y_obs, predictions=y_pred, ax=ax)
            fig.savefig(f"figs/{normalization}_{method}.png")

        fig.suptitle("Conclusions rock!")


plt.show()
