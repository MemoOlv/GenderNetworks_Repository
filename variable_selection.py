#! /usr/bin/python

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import typer

import lib.data_processing_functions as dpf

app = typer.Typer()


@app.command()
def variable_selection(year: int):
    lib_path = "/lib"
    sys.path.insert(0, lib_path)

    sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})
    data_path = "data/"
    yr = str(year)

    # Read ENIGH clean data
    ENIGHr = pd.read_csv(data_path + "ENIGH" + yr + "_clean.csv", index_col=[0])
    ENIGH = ENIGHr.copy()

    # Add columns to ENIGH for data classification
    t = "CH"  # Options CH,CP,MEPI
    ENIGH = dpf.hhld_classification(ENIGH)

    # Computation of the representativity
    # 0->cov_matrix 1->keys, 2>represent, 3->n_nodes
    R = dpf.ComputeRepresentativity(ENIGH, t, yr, data_path)

    # frames0 is a list that contains the criteria selection
    frames0 = list()
    for i in range(0, len(R[2])):
        frames0.append(dpf.criteria(R[2], R[1][i], R[3])[0])
    # frames1 is a dictionary that contains the covariance data
    frames1 = {}
    for i in range(0, len(R[2])):
        frames1[R[1][i]] = dpf.criteria(R[2], R[1][i], R[3])[1]
    crt = pd.concat(frames0, ignore_index=True)

    k = R[1][0]  # Select the person classification to plot
    crt_p = frames1[k]
    crt_pmax = crt_p[crt_p["covmul"] == crt_p["covmul"].max()]
    m = crt.value.mean()
    crt_sort = crt.sort_values(by="num")

    f = plt.figure(figsize=(12, 8))
    f.subplots_adjust(hspace=0.0)
    fontsize_ticks = 20
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])
    ax.tick_params(labelsize=fontsize_ticks)
    sns.despine()
    sns.scatterplot(data=crt_p, x="cov", y="covmul", alpha=0.8, size="covmul", hue="covmul", ax=ax)
    sns.scatterplot(data=crt_pmax, x="cov", y="covmul", color="red", ax=ax, label="$x_{m}$")
    ax.legend(loc="best", frameon=True, fontsize=(fontsize_ticks - 5), title="Rep*Cov")
    plt.xlabel("Cov", fontsize=fontsize_ticks)
    plt.ylabel("Rep*Cov", fontsize=fontsize_ticks)
    plt.savefig("reports/figures/RepCov_HAdultos" + yr + ".pdf", bbox_inches="tight")
    plt.show()

    f = plt.figure(figsize=(8 * 1.6, 8))
    f.subplots_adjust(hspace=0.0)
    fontsize_ticks = 20
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])
    ax.tick_params(labelsize=fontsize_ticks)
    sns.despine()
    sns.scatterplot(data=crt_p, x="idx", y=k, alpha=0.8, size="cov", hue="cov", ax=ax)
    # sns.scatterplot(data=crt_pmax, x='idx', y=k, color='red',ax=ax)
    for line in range(0, 13):
        n_s = dpf.recur_fibo(line)
        plt.text(crt_p.idx[n_s], crt_p[k][n_s], crt_p.index[n_s], horizontalalignment="center")
    plt.xlabel("No. Variable", fontsize=fontsize_ticks)
    plt.ylabel("Rep", fontsize=fontsize_ticks)
    ax.legend(loc="best", frameon=True, fontsize=(fontsize_ticks - 5), title="Cov")
    plt.yscale("log")
    plt.xscale("log")
    plt.savefig("reports/figures/Representatividad_HAdultos" + yr + ".pdf", bbox_inches="tight")
    plt.show()

    f = plt.figure(figsize=(10 * 1.618, 8))
    f.subplots_adjust(hspace=0.0)
    fontsize_ticks = 20
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])
    ax.tick_params("y", labelsize=fontsize_ticks)
    sns.despine()
    new_ticks = [i for i in crt_sort.PC]
    plt.xticks(
        range(0, len(new_ticks), 3), new_ticks[::3], fontsize=(fontsize_ticks - 5), rotation=90
    )
    ax = sns.lineplot(data=crt_sort, x="PC", y="value", marker="o", label="Rep$_{m}$")
    ax2 = ax.twinx()
    ax2.tick_params(labelsize=fontsize_ticks)
    sns.lineplot(
        data=crt_sort, x="PC", y="num", ax=ax2, color="green", marker="o", label="No. personas"
    )
    ax.axhline(y=m, linestyle="--", color="darkblue")
    ax.set_ylabel("Rep", fontsize=fontsize_ticks)
    ax.set_xlabel("", fontsize=fontsize_ticks)
    ax2.set_ylabel("Número de personas", fontsize=fontsize_ticks)
    ax.set_ylim((0, 1.05))
    ax2.set_ylim((0, 100000))
    ax.legend(loc="upper left", frameon=True)
    plt.savefig("reports/figures/Rep_Pob_Hogares" + yr + ".pdf", bbox_inches="tight")
    plt.show()

    # print(R[1])

    # print(frames1)
    cov_matrix_cut = dpf.typeofcriteria(R[1], "static", frames1, m, crt)
    # cov_matrix_cut.drop('foliohog',inplace=True)

    f = plt.figure(figsize=(30, 30))
    f.subplots_adjust(hspace=0.0)
    fontsize_ticks = 25
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])
    ax.tick_params(labelsize=fontsize_ticks)
    sns.heatmap(cov_matrix_cut, cmap="jet")
    cax = plt.gcf().axes[-1]
    cax.tick_params(labelsize=fontsize_ticks)
    plt.savefig("reports/figures/CovMatrixCut" + yr + ".pdf", bbox_inches="tight")
    plt.show()

    cov_matrix_cut.to_csv(data_path + "cov_matrix_" + t + yr + "_cut.csv", index=True)


if __name__ == "__main__":
    typer.run(variable_selection)
