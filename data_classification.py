#! /usr/bin/python

import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import multivariate_normal

import lib.data_processing_functions as dpf

lib_path = "lib"
sys.path.insert(0, lib_path)


sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})

data_path = "data/"
yr = "2016"  # choices are 2016, 2018 and 2020

ENIGHr = pd.read_csv(data_path + "ENIGH" + yr + "_clean.csv", index_col=[0])
ENIGH = ENIGHr.copy()

ENIGH = dpf.hhld_classification(ENIGH)

ps_list = ENIGH.node.unique()
ENIGH["count_node"] = ENIGH.groupby("node")["node"].transform("count")
d = ENIGH.sort_values(by=["count_node"], ignore_index=True)

f = plt.figure(figsize=(20, 8))
f.subplots_adjust(hspace=0.0)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.set_color_codes("muted")
sns.histplot(y="age_habit", data=d[d.sex_hhrp == "H"], color="y", label="Hombre", alpha=0.7)
sns.set_color_codes("muted")
sns.histplot(y="age_habit", data=d[d.sex_hhrp == "M"], color="b", label="Mujer", alpha=0.7)
ax.legend(loc="best", frameon=True, fontsize=fontsize_ticks)
plt.xscale("log")
plt.xlabel("Número de personas", fontsize=fontsize_ticks)
plt.ylabel("")
plt.savefig("reports/figures/CH_NumPersonas" + yr + ".pdf", bbox_inches="tight")
plt.show()

ENIGH.drop(columns=["sex_hhrp", "age_habit"], inplace=True)
t = "CH"
ENIGH.to_csv(data_path + "/ENIGH_" + t + yr + ".csv", index=True)

personclass = {}
for ps in ENIGH.node.unique():
    personclass[ps] = ENIGH[ENIGH.node == ps]
# stadardization in dictionary
personclass_std = {}
ps_newlist = list()
for ps in ps_list:
    df = dpf.standardization(personclass[ps])
    if (len(df.columns) > 1) & (any(df.columns.str.contains("energia"))):
        personclass_std[ps] = df
        ps_newlist.append(ps)

ps_df = personclass["HAdultosMenores"].reset_index(drop=True)
ps_std_df = personclass_std["HAdultosMenores"].reset_index(drop=True)

cov_mtx = np.cov(ps_std_df.ing_cor, ps_std_df.energia)
mean1 = ps_std_df.ing_cor.mean()
mean2 = ps_std_df.energia.mean()
x, y = np.mgrid[-2:15:0.01, -2:15:0.01]
pos = np.dstack((x, y))
rv = multivariate_normal([mean1, mean2], cov_mtx)

fig, ax = plt.subplots(figsize=(8, 8))
ax.contourf(x, y, rv.pdf(pos), cmap="YlOrBr")
sns.scatterplot(
    data=ps_std_df,
    x="ing_cor",
    y="energia",
    color="lightgreen",
    alpha=0.1,
    size=0.005,
    edgecolor=None,
)
ax.set_xlim((-2, 15))
ax.set_ylim((-2, 15))
ax.set_ylabel("Z score Energia (-)", fontsize=fontsize_ticks)
ax.set_xlabel("Z score Ingreso corriente (-)", fontsize=fontsize_ticks)
axins = ax.inset_axes([0.5, 0.5, 0.47, 0.47])
axins.contourf(x, y, rv.pdf(pos), cmap="YlOrBr")
x1, x2, y1, y2 = -2, 2, -2, 2
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
ax.indicate_inset_zoom(axins, edgecolor="black")
ax.get_legend().remove()
plt.savefig("reports/figures/Energia_Corriente_Zscore.png", bbox_inches="tight", dpi=100)
plt.show()

cov_mtx = np.cov(ps_std_df.alfabetism, ps_std_df.energia)
mean1 = ps_std_df.alfabetism.mean()
mean2 = ps_std_df.alfabetism.mean()
x, y = np.mgrid[-2:15:0.01, -2:15:0.01]
pos = np.dstack((x, y))
rv = multivariate_normal([mean1, mean2], cov_mtx)

fig, ax = plt.subplots(figsize=(8, 8))
ax.contourf(x, y, rv.pdf(pos), cmap="YlOrBr")
sns.scatterplot(
    data=ps_std_df,
    x="alfabetism",
    y="energia",
    color="lightgreen",
    alpha=0.1,
    size=0.005,
    edgecolor=None,
)
ax.set_xlim((-2, 15))
ax.set_ylim((-2, 15))
ax.set_ylabel("Z score Energia (-)", fontsize=fontsize_ticks)
ax.set_xlabel("Z score Alfabetismo  (-)", fontsize=fontsize_ticks)
axins = ax.inset_axes([0.5, 0.5, 0.47, 0.47])
axins.contourf(x, y, rv.pdf(pos), cmap="YlOrBr")
x1, x2, y1, y2 = -2, 2, -2, 2
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
ax.indicate_inset_zoom(axins, edgecolor="black")
ax.get_legend().remove()
plt.savefig("reports/figures/Energia_Alfabetismo_Zscore.png", bbox_inches="tight", dpi=100)
plt.show()

f = plt.figure(figsize=(8 * 1.6, 8))
f.subplots_adjust(hspace=0.0)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.scatterplot(
    data=ps_df, x="ing_cor", y="energia", ax=ax, color="blue", alpha=0.5, edgecolor=None
)
ax2 = ax.twiny()
ax2.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(
    data=ps_df, x="alfabetism", y="energia", ax=ax2, color="orange", alpha=0.5, edgecolor=None
)
ax.set_xlim((-5, 1650000))
ax2.set_xlim((-5, 1650000))
ax.set_ylabel("Energia (MXN)", fontsize=fontsize_ticks)
ax.set_xlabel("Ingreso corriente (MXN)", fontsize=fontsize_ticks)
ax2.set_xlabel("Alfabetismo (-)", fontsize=fontsize_ticks)
plt.savefig("reports/figures/Energia_Alfabetismo_Diferencias.png", bbox_inches="tight", dpi=50)
plt.show()

f = plt.figure(figsize=(8 * 1.6, 8))
f.subplots_adjust(hspace=0.0)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.scatterplot(data=ps_std_df, x="ing_cor", y="energia", ax=ax, color="blue", edgecolor=None)
ax2 = ax.twiny()
ax2.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(data=ps_std_df, x="alfabetism", y="energia", ax=ax2, color="orange", edgecolor=None)
ax.set_xlim((-1, 30))
ax2.set_xlim((-1, 30))
ax.set_ylabel("Z score Energia (-)", fontsize=fontsize_ticks)
ax.set_xlabel("Z score Ingreso corriente (-)", fontsize=fontsize_ticks)
ax2.set_xlabel("Z score Alfabetismo (-)", fontsize=fontsize_ticks)
plt.savefig(
    "reports/figures/Energia_Alfabetismp_Diferencias_Zscore.png", bbox_inches="tight", dpi=50
)
plt.show()

personclass_energy = {}
for ps in ps_newlist:
    personclass_energy[ps] = abs(personclass_std[ps].cov().energia)
    personclass_energy[ps].drop(["energia", "vivienda"], inplace=True)

series = list()
for ps in ps_newlist:
    sx = personclass_energy[ps]
    sx.rename(ps, inplace=True)
    series.append(sx)

cov_matrix_CH = pd.concat(series, axis=1).fillna(0)

f = plt.figure(figsize=(30, 30))
f.subplots_adjust(hspace=0.0)
fontsize_ticks = 25
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.heatmap(cov_matrix_CH, cmap="jet")
cax = plt.gcf().axes[-1]
cax.tick_params(labelsize=fontsize_ticks)
plt.savefig("reports/figures/CovMatrix_Heatmap" + yr + ".pdf", bbox_inches="tight")
plt.show()

# Save covariance matrix Household Classification
t = "CH"
cov_matrix_CH.to_csv(data_path + "cov_matrix_" + t + yr + ".csv", index=True)
