#! /usr/bin/python

import sys
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import random

import lib.network_analysis_functions as naf

lib_path = "/lib"
sys.path.insert(0, lib_path)


sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})

data_path = "data/"
t = "CH"  # Options CH, CP, MEPI
crit = "static"  # Options static, dynamic
seed = 100

# Read data classification
var_class = pd.read_csv(data_path + "/VariableClassification.csv", usecols=["Type", "Variable"])
var_class.set_index("Variable", inplace=True)

cov_matrix2016 = pd.read_csv(data_path + "cov_matrix_" + t + "2016" + "_cut.csv", index_col=[0])
cov_matrix2018 = pd.read_csv(data_path + "cov_matrix_" + t + "2018" + "_cut.csv", index_col=[0])
cov_matrix2020 = pd.read_csv(data_path + "cov_matrix_" + t + "2020" + "_cut.csv", index_col=[0])

Network2016 = naf.network_construction(cov_matrix2016)
Network2018 = naf.network_construction(cov_matrix2018)
Network2020 = naf.network_construction(cov_matrix2020)

color_map = []
for node in Network2016[0]:
    if node in Network2016[1]:
        color_map.append("darkcyan")
    else:
        color_map.append("orange")
top_nodes, botm_nodes = bipartite.sets(Network2016[0])

with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        Network2016[0],
        with_labels=False,
        node_color=color_map,
        node_size=100,
        alpha=0.7,
        edge_color="lightgray",
        pos=nx.fruchterman_reingold_layout(Network2016[0], seed=seed),
    )
plt.savefig("reports/figures/RedCH" + "2016" + ".pdf", bbox_inches="tight")
plt.show()

naf.global_properties(Network2016, top_nodes, botm_nodes)

color_map = []
for node in Network2018[0]:
    if node in Network2018[1]:
        color_map.append("darkcyan")
    else:
        color_map.append("orange")
top_nodes, botm_nodes = bipartite.sets(Network2018[0])

with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        Network2018[0],
        with_labels=False,
        node_color=color_map,
        node_size=100,
        alpha=0.7,
        edge_color="lightgray",
        pos=nx.fruchterman_reingold_layout(Network2018[0], seed=seed),
    )
plt.savefig("reports/figures/RedCH" + "2018" + ".pdf", bbox_inches="tight")
plt.show()

naf.global_properties(Network2018, top_nodes, botm_nodes)

color_map = []
for node in Network2020[0]:
    if node in Network2020[1]:
        color_map.append("darkcyan")
    else:
        color_map.append("orange")
top_nodes, botm_nodes = bipartite.sets(Network2020[0])

with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        Network2020[0],
        with_labels=False,
        node_color=color_map,
        node_size=100,
        alpha=0.7,
        edge_color="lightgray",
        pos=nx.fruchterman_reingold_layout(Network2020[0], seed=seed),
    )
plt.savefig("reports/figures/RedCH" + "2020" + ".pdf", bbox_inches="tight")
plt.show()

naf.global_properties(Network2020, top_nodes, botm_nodes)

Fuerza2016 = naf.df_prop_nodes(Network2016, "2016", top_nodes)
Fuerza2018 = naf.df_prop_nodes(Network2018, "2018", top_nodes)
Fuerza2020 = naf.df_prop_nodes(Network2020, "2020", top_nodes)
Fuerza = pd.concat([Fuerza2016, Fuerza2018, Fuerza2020], ignore_index=True)

f = plt.figure(figsize=(8 * 1.618, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.scatterplot(
    data=Fuerza, x=Fuerza.index, y="Fuerza", hue="Año", style="Tipo", s=60, markers=["X", "o"]
)
plt.xlabel("Ordenados por coeficiente de clustering", fontsize=fontsize_ticks)
plt.ylabel("$s$", fontsize=fontsize_ticks)
x_ticks = [1, 175, 175 + 183, 175 + 183 + 164]
x_labels = ["1", "175", "183", "164"]
plt.xticks(ticks=x_ticks, labels=x_labels)
plt.yscale("log")
ax.legend(fontsize=13, framealpha=0.1)
ax.text(45, 2.5, "b", fontsize=fontsize_ticks, family="serif")
ax.text(230, 2.5, "b", fontsize=fontsize_ticks, family="serif")
ax.text(415, 2.5, "b", fontsize=fontsize_ticks, family="serif")
ax.text(20, 0.18, "a", fontsize=fontsize_ticks, family="serif")
ax.text(190, 0.18, "a", fontsize=fontsize_ticks, family="serif")
ax.text(370, 0.18, "a", fontsize=fontsize_ticks, family="serif")
ax.text(155, 4, "c", fontsize=fontsize_ticks, family="serif")
ax.text(340, 4, "c", fontsize=fontsize_ticks, family="serif")
ax.text(500, 4, "c", fontsize=fontsize_ticks, family="serif")
ax.text(55, 25, "A", fontsize=fontsize_ticks, family="serif")
ax.text(200, 25, "A", fontsize=fontsize_ticks, family="serif")
ax.text(400, 25, "A", fontsize=fontsize_ticks, family="serif")
ax.text(170, 20, "B", fontsize=fontsize_ticks, family="serif")
ax.text(360, 20, "B", fontsize=fontsize_ticks, family="serif")
ax.text(500, 18, "B", fontsize=fontsize_ticks, family="serif")
plt.savefig("reports/figures/xFuerzayOrden_anios.pdf", bbox_inches="tight")
plt.show()

Fuerza2016 = Fuerza[Fuerza.Año == "2016"]
x = plt.hist(Fuerza2016.Grado, bins=200, density=True)
xx = plt.hist(Fuerza2016.Fuerza, bins=200, density=True)
equis = [x[1][i] + (x[1][1] - x[1][0]) for i in range(0, len(x[1]) - 1)]
equis_2 = [xx[1][i] + (xx[1][1] - xx[1][0]) for i in range(0, len(xx[1]) - 1)]
d2016 = pd.DataFrame(
    {"Grado": x[0], "x_grado": equis, "Fuerza": xx[0], "x_fuerza": equis_2, "Año": "2016"}
)

Fuerza2018 = Fuerza[Fuerza.Año == "2018"]
x = plt.hist(Fuerza2018.Grado, bins=200, density=True)
xx = plt.hist(Fuerza2018.Fuerza, bins=200, density=True)
equis = [x[1][i] + (x[1][1] - x[1][0]) for i in range(0, len(x[1]) - 1)]
equis_2 = [xx[1][i] + (xx[1][1] - xx[1][0]) for i in range(0, len(xx[1]) - 1)]
d2018 = pd.DataFrame(
    {"Grado": x[0], "x_grado": equis, "Fuerza": xx[0], "x_fuerza": equis_2, "Año": "2018"}
)

Fuerza2020 = Fuerza[Fuerza.Año == "2020"]
x = plt.hist(Fuerza2020.Grado, bins=200, density=True)
xx = plt.hist(Fuerza2020.Fuerza, bins=200, density=True)
equis = [x[1][i] + (x[1][1] - x[1][0]) for i in range(0, len(x[1]) - 1)]
equis_2 = [xx[1][i] + (xx[1][1] - xx[1][0]) for i in range(0, len(xx[1]) - 1)]
d2020 = pd.DataFrame(
    {"Grado": x[0], "x_grado": equis, "Fuerza": xx[0], "x_fuerza": equis_2, "Año": "2020"}
)

d = pd.concat([d2016, d2018, d2020], ignore_index=True)

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.scatterplot(
    data=d, x="x_grado", y="Grado", hue="Año", style="Año", s=80, alpha=0.7, edgecolor="black"
)
ax.set(yscale="log", ylim=(0.01, 1.2), xscale="log", xlim=(0.5, 250))
plt.xlabel("$k$", fontsize=fontsize_ticks)
plt.ylabel("$p(k)$", fontsize=fontsize_ticks)
ax.legend(fontsize=13, framealpha=0.1)
plt.savefig("reports/figures/P_k.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.scatterplot(
    data=d, x="x_fuerza", y="Fuerza", hue="Año", style="Año", s=80, alpha=0.7, edgecolor="black"
)
ax.set(yscale="log", ylim=(0.01, 1.2), xscale="log", xlim=(0.1, 250))
plt.xlabel("$s$", fontsize=fontsize_ticks)
plt.ylabel("$p(s)$", fontsize=fontsize_ticks)
ax.legend(fontsize=13, framealpha=0.1)
plt.savefig("reports/figures/P_s.pdf", bbox_inches="tight")
plt.show()

random.seed(seed)

C2016 = naf.Community_Detection(Network2016)
C2018 = naf.Community_Detection(Network2018)
C2020 = naf.Community_Detection(Network2020)

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(
    data=C2016[1],
    x=C2016[1].index,
    y="Modularidad",
    hue="No Comunidades",
    size="No Comunidades",
    style="No Comunidades",
    palette="Set2",
    edgecolor=None,
)
plt.xlabel("No iteración", fontsize=fontsize_ticks)
plt.ylabel("$Q$", fontsize=fontsize_ticks)
plt.savefig("reports/figures/Comunidades_iter2016.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(
    data=C2018[1],
    x=C2018[1].index,
    y="Modularidad",
    hue="No Comunidades",
    size="No Comunidades",
    style="No Comunidades",
    palette="Set2",
    edgecolor=None,
)
plt.xlabel("No iteración", fontsize=fontsize_ticks)
plt.ylabel("$Q$", fontsize=fontsize_ticks)
plt.savefig("reports/figures/Comunidades_iter2018.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(
    data=C2020[1],
    x=C2020[1].index,
    y="Modularidad",
    hue="No Comunidades",
    size="No Comunidades",
    style="No Comunidades",
    palette="Set2",
    edgecolor=None,
)
plt.xlabel("No iteración", fontsize=fontsize_ticks)
plt.ylabel("$Q$", fontsize=fontsize_ticks)
plt.savefig("reports/figures/Comunidades_iter2020.pdf", bbox_inches="tight")
plt.show()

color_map = naf.colors_community(Network2016[0], C2016[0])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        Network2016[0],
        with_labels=False,
        node_size=100,
        alpha=0.7,
        edge_color="lightgray",
        node_color=color_map,
        pos=nx.fruchterman_reingold_layout(Network2016[0], seed=seed),
    )
plt.savefig("reports/figures/Comunidades_color2016.pdf", bbox_inches="tight")
plt.show()

color_map = naf.colors_community(Network2018[0], C2018[0])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        Network2018[0],
        with_labels=False,
        node_size=100,
        alpha=0.7,
        edge_color="lightgray",
        node_color=color_map,
        pos=nx.fruchterman_reingold_layout(Network2018[0], seed=seed),
    )
plt.savefig("reports/figures/Comunidades_color2018.pdf", bbox_inches="tight")
plt.show()

color_map = naf.colors_community(Network2020[0], C2020[0])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        Network2020[0],
        with_labels=False,
        node_size=100,
        alpha=0.7,
        edge_color="lightgray",
        node_color=color_map,
        pos=nx.fruchterman_reingold_layout(Network2020[0], seed=seed),
    )
plt.savefig("reports/figures/Comunidades_color2020.pdf", bbox_inches="tight")
plt.show()

cov_matrix2016 = pd.read_csv(data_path + "cov_matrix_" + t + "2016" + "_cut.csv", index_col=[0])
cov_matrix2018 = pd.read_csv(data_path + "cov_matrix_" + t + "2018" + "_cut.csv", index_col=[0])
cov_matrix2020 = pd.read_csv(data_path + "cov_matrix_" + t + "2020" + "_cut.csv", index_col=[0])

CH_codes = {
    "MAdultos": "M1",
    "MAdultosMenores": "M2",
    "MAdultosMayores": "M3",
    "MMayoresMenores": "M4",
    "MMayores": "M5",
    "MAdultosMayoresMenores": "M6",
    "HAdultos": "H1",
    "HAdultosMenores": "H2",
    "HAdultosMayores": "H3",
    "HMayoresMenores": "H4",
    "HMayores": "H5",
    "HAdultosMayoresMenores": "H6",
}

cov_matrix2016.rename(columns=CH_codes, inplace=True)
cov_matrix2018.rename(columns=CH_codes, inplace=True)
cov_matrix2020.rename(columns=CH_codes, inplace=True)
Network2016 = naf.network_construction(cov_matrix2016)
Network2018 = naf.network_construction(cov_matrix2018)
Network2020 = naf.network_construction(cov_matrix2020)
C2016 = naf.Community_Detection(Network2016)
C2018 = naf.Community_Detection(Network2018)
C2020 = naf.Community_Detection(Network2020)

Nodes2016 = list(Network2016[0].nodes)
Nodes2018 = list(Network2018[0].nodes)
Nodes2020 = list(Network2020[0].nodes)
Nodes2016 = pd.DataFrame({"Nodes": Nodes2016, "Año": "2016", "Presencia": "0"})
Nodes2018 = pd.DataFrame({"Nodes": Nodes2018, "Año": "2018", "Presencia": "0"})
Nodes2020 = pd.DataFrame({"Nodes": Nodes2020, "Año": "2020", "Presencia": "0"})
Nodesyr = pd.concat([Nodes2016, Nodes2018, Nodes2020], ignore_index=True)
Nodesyr["Presencia"] = Nodesyr.Nodes.apply(lambda x: (Nodesyr.Nodes == x).sum())
Nodesyr["Type"] = Nodesyr.Nodes.apply(lambda x: var_class.loc[x].Type)
Nodesyr.sort_values(by=["Presencia", "Año", "Type"], ascending=[False, True, True], inplace=True)

naf.Dynamic_coefficients(Nodes2016.Nodes, Nodes2018.Nodes)
naf.Dynamic_coefficients(Nodes2018.Nodes, Nodes2020.Nodes)
naf.Dynamic_coefficients(Nodes2016.Nodes, Nodes2020.Nodes)

f = plt.figure(figsize=(8, 8 * 1.618))
f.subplots_adjust(hspace=0.0)
fontsize_ticks = 10 + 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
# ax.hlines(y='H1',xmin='2016',xmax='2018')
# ax.hlines(y='H1',xmin='2020',xmax='2018')
sns.stripplot(data=Nodesyr, x="Año", y="Nodes", hue="Presencia", ax=ax, s=10, linewidth=1)
plt.xlabel("Año", fontsize=fontsize_ticks)
plt.ylabel("Nodos", fontsize=fontsize_ticks)
plt.yticks([])
ax.legend(fontsize=20, framealpha=1, title="Años", title_fontsize=20)
plt.savefig("reports/figures/Nodes_dynamic.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(25 * 0.623, 25))
f.subplots_adjust(hspace=0.0)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
# ax.hlines(y='H1',xmin='2016',xmax='2018')
# ax.hlines(y='H1',xmin='2020',xmax='2018')
sns.stripplot(data=Nodesyr, x="Año", y="Nodes", hue="Presencia", ax=ax, s=10, linewidth=1)

plt.xlabel("Año", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks + 10)
plt.yticks(fontsize=fontsize_ticks - 3)
plt.xticks(fontsize=fontsize_ticks + 5)
ax.legend(fontsize=20, framealpha=1, title="Presencia", title_fontsize=20)
plt.savefig("reports/figures/Nodes_dynamic_detailed.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.histplot(
    data=Nodesyr[Nodesyr.Type != "CH"].sort_values(by="Año", ascending=True),
    x="Año",
    y="Type",
    palette="Set2",
    discrete=(True, True),
    cbar=True,
    cbar_kws=dict(shrink=0.75),
    stat="count",
)
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 5)
plt.yticks(fontsize=fontsize_ticks + 5)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks + 10)
plt.savefig("reports/figures/Heatvariables_redcompleta.pdf", bbox_inches="tight")
plt.show()

c1_2016 = list(C2016[0][0])
c1_2018 = list(C2018[0][0])
c1_2020 = list(C2020[0][0])
c1_2016 = pd.DataFrame({"Nodes": c1_2016, "Año": "2016", "Presencia": "0"})
c1_2018 = pd.DataFrame({"Nodes": c1_2018, "Año": "2018", "Presencia": "0"})
c1_2020 = pd.DataFrame({"Nodes": c1_2020, "Año": "2020", "Presencia": "0"})
Group1 = pd.concat([c1_2016, c1_2018, c1_2020], ignore_index=True)
Group1["Presencia"] = Group1.Nodes.apply(lambda x: str((Group1.Nodes == x).sum()))
Group1["Type"] = Group1.Nodes.apply(lambda x: var_class.loc[x].Type)
Group1.sort_values(by=["Presencia", "Año", "Type"], ascending=[True, True, True], inplace=True)

naf.Dynamic_coefficients(c1_2016.Nodes, c1_2018.Nodes)  # 2016-2018
naf.Dynamic_coefficients(c1_2018.Nodes, c1_2020.Nodes)  # 2018-2020
naf.Dynamic_coefficients(c1_2016.Nodes, c1_2020.Nodes)  # 2016-2020

f = plt.figure(figsize=(5, 22))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(data=Group1, x="Año", y="Nodes", hue="Presencia", ax=ax, s=150, edgecolor="black")
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 10)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks)
ax.legend(fontsize=15, framealpha=0.1, title_fontsize=13, title="Años")
plt.savefig("reports/figures/Nodes_dynamics_G1.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.histplot(
    data=Group1[Group1.Type != "CH"],
    x="Año",
    y="Type",
    palette="Set2",
    discrete=(True, True),
    cbar=True,
    cbar_kws=dict(shrink=0.75),
)
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 5)
plt.yticks(fontsize=fontsize_ticks + 5)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks + 10)
plt.savefig("reports/figures/Heatvariables_G1.pdf", bbox_inches="tight")
plt.show()

c2_2016 = list(C2016[0][1])
c4_2018 = list(C2018[0][3])
c4_2020 = list(C2020[0][3])
c2_2016 = pd.DataFrame({"Nodes": c2_2016, "Año": "2016", "Presencia": "0"})
c4_2018 = pd.DataFrame({"Nodes": c4_2018, "Año": "2018", "Presencia": "0"})
c4_2020 = pd.DataFrame({"Nodes": c4_2020, "Año": "2020", "Presencia": "0"})
Group2 = pd.concat([c2_2016, c4_2018, c4_2020], ignore_index=True)
Group2["Presencia"] = Group2.Nodes.apply(lambda x: str((Group2.Nodes == x).sum()))
Group2["Type"] = Group2.Nodes.apply(lambda x: var_class.loc[x].Type)
Group2.sort_values(by=["Presencia", "Año", "Type"], ascending=[True, True, True], inplace=True)

naf.Dynamic_coefficients(c2_2016.Nodes, c4_2018.Nodes)  # 2016-2018
naf.Dynamic_coefficients(c4_2018.Nodes, c4_2020.Nodes)  # 2018-2020
naf.Dynamic_coefficients(c2_2016.Nodes, c4_2020.Nodes)  # 2016-2020

f = plt.figure(figsize=(5, 22))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(data=Group2, x="Año", y="Nodes", hue="Presencia", ax=ax, s=150, edgecolor="black")
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 10)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks)
ax.legend(fontsize=15, framealpha=0.1, title_fontsize=13, title="Años")
plt.savefig("reports/figures/Nodes_dynamics_G2.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.histplot(
    data=Group2[Group2.Type != "CH"],
    x="Año",
    y="Type",
    palette="Set2",
    discrete=(True, True),
    cbar=True,
    cbar_kws=dict(shrink=0.75),
)
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 5)
plt.yticks(fontsize=fontsize_ticks + 5)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks + 10)
plt.savefig("reports/figures/Heatvariables_G2.pdf", bbox_inches="tight")
plt.show()

c3_2016 = list(C2016[0][2])
c2_2018 = list(C2018[0][1])
c2_2020 = list(C2020[0][1])
c3_2016 = pd.DataFrame({"Nodes": c3_2016, "Año": "2016", "Presencia": "0"})
c2_2018 = pd.DataFrame({"Nodes": c2_2018, "Año": "2018", "Presencia": "0"})
c2_2020 = pd.DataFrame({"Nodes": c2_2020, "Año": "2020", "Presencia": "0"})
Group3 = pd.concat([c3_2016, c2_2018, c2_2020], ignore_index=True)
Group3["Presencia"] = Group3.Nodes.apply(lambda x: str((Group3.Nodes == x).sum()))
Group3["Type"] = Group3.Nodes.apply(lambda x: var_class.loc[x].Type)
Group3.sort_values(by=["Presencia", "Año", "Type"], ascending=[True, True, True], inplace=True)

naf.Dynamic_coefficients(c3_2016.Nodes, c2_2018.Nodes)  # 2016-2018
naf.Dynamic_coefficients(c2_2018.Nodes, c2_2020.Nodes)  # 2018-2020
naf.Dynamic_coefficients(c3_2016.Nodes, c2_2020.Nodes)  # 2016-2020

f = plt.figure(figsize=(5, 22))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(data=Group3, x="Año", y="Nodes", hue="Presencia", ax=ax, s=150, edgecolor="black")
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 10)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks)
ax.legend(fontsize=15, framealpha=0.1, title_fontsize=13, title="Años")
plt.savefig("reports/figures/Nodes_dynamics_G3.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.histplot(
    data=Group3[Group3.Type != "CH"],
    x="Año",
    y="Type",
    palette="Set2",
    discrete=(True, True),
    cbar=True,
    cbar_kws=dict(shrink=0.75),
)
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 5)
plt.yticks(fontsize=fontsize_ticks + 5)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks + 10)
plt.savefig("reports/figures/Heatvariables_G3.pdf", bbox_inches="tight")
plt.show()

c4_2016 = list(C2016[0][3])
c3_2018 = list(C2018[0][2])
c3_2020 = list(C2020[0][2])
c4_2016 = pd.DataFrame({"Nodes": c4_2016, "Año": "2016", "Presencia": "0"})
c3_2018 = pd.DataFrame({"Nodes": c3_2018, "Año": "2018", "Presencia": "0"})
c3_2020 = pd.DataFrame({"Nodes": c3_2020, "Año": "2020", "Presencia": "0"})
Group4 = pd.concat([c4_2016, c3_2018, c3_2020], ignore_index=True)
Group4["Presencia"] = Group4.Nodes.apply(lambda x: str((Group4.Nodes == x).sum()))
Group4["Type"] = Group4.Nodes.apply(lambda x: var_class.loc[x].Type)
Group4.sort_values(by=["Presencia", "Año", "Type"], ascending=[True, True, True], inplace=True)

naf.Dynamic_coefficients(c4_2016.Nodes, c3_2018.Nodes)  # 2016-2018
naf.Dynamic_coefficients(c3_2018.Nodes, c3_2020.Nodes)  # 2018-2020
naf.Dynamic_coefficients(c4_2016.Nodes, c3_2020.Nodes)  # 2016-2020

f = plt.figure(figsize=(5, 22))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.scatterplot(data=Group4, x="Año", y="Nodes", hue="Presencia", ax=ax, s=150, edgecolor="black")
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 10)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks)
ax.legend(fontsize=15, framealpha=0.1, title_fontsize=13, title="Años")
plt.savefig("reports/figures/Nodes_dynamics_G4.pdf", bbox_inches="tight")
plt.show()

f = plt.figure(figsize=(8, 8))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 10
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(labelsize=fontsize_ticks)
sns.histplot(
    data=Group4[Group4.Type != "CH"],
    x="Año",
    y="Type",
    palette="Set2",
    discrete=(True, True),
    cbar=True,
    cbar_kws=dict(shrink=0.75),
)
plt.xticks(["2016", "2018", "2020"], fontsize=fontsize_ticks + 5)
plt.yticks(fontsize=fontsize_ticks + 5)
plt.xlabel("", fontsize=fontsize_ticks + 10)
plt.ylabel("", fontsize=fontsize_ticks + 10)
plt.savefig("reports/figures/Heatvariables_G4.pdf", bbox_inches="tight")
plt.show()

c2016_1 = nx.subgraph(Network2016[0], C2016[0][0])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2016_1,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="blue",
        pos=nx.fruchterman_reingold_layout(c2016_1, seed=seed),
    )
plt.title("Comunidad 1")
plt.savefig("reports/figures/C1_2016.pdf", bbox_inches="tight")
plt.show()

vars_c2016_1 = naf.community_description(c2016_1, var_class)
vars_c2016_1.to_csv(data_path + "socialframeworkvariables/c2016_1.csv")

# Community 2-2016

c2016_2 = nx.subgraph(Network2016[0], C2016[0][1])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8.2 * 1.618, 8.2))
    ax.axis("off")
    nx.draw_networkx(
        c2016_2,
        with_labels=True,
        node_size=150,
        alpha=1,
        edge_color="lightgray",
        node_color="orange",
        pos=nx.fruchterman_reingold_layout(c2016_2, seed=seed),
        font_size=8,
    )
plt.title("Comunidad 2")
plt.savefig("reports/figures/C2_2016.pdf", bbox_inches="tight")
plt.show()

vars_c2016_2 = naf.community_description(c2016_2, var_class)
vars_c2016_2.to_csv(data_path + "socialframeworkvariables/c2016_2.csv")

# Community 3-2016

c2016_3 = nx.subgraph(Network2016[0], C2016[0][2])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2016_3,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="green",
        pos=nx.fruchterman_reingold_layout(c2016_3, seed=seed),
    )
plt.title("Comunidad 3")
plt.savefig("reports/figures/C3_2016.pdf", bbox_inches="tight")
plt.show()

vars_c2016_3 = naf.community_description(c2016_3, var_class)
vars_c2016_3.to_csv(data_path + "/socialframeworkvariables/c2016_3.csv")

# Community 4-2016

c2016_4 = nx.subgraph(Network2016[0], C2016[0][3])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2016_4,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="red",
        pos=nx.fruchterman_reingold_layout(c2016_4, seed=seed),
    )
plt.title("Comunidad 4")
plt.savefig("reports/figures/C4_2016.pdf", bbox_inches="tight")
plt.show()

vars_c2016_4 = naf.community_description(c2016_4, var_class)
vars_c2016_4.to_csv(data_path + "/socialframeworkvariables/c2016_4.csv")

# Community 1-2018

c2018_1 = nx.subgraph(Network2018[0], C2018[0][0])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2018_1,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="blue",
        pos=nx.fruchterman_reingold_layout(c2018_1, seed=seed),
    )
plt.title("Comunidad 1")
plt.savefig("reports/figures/C1_2018.pdf", bbox_inches="tight")
plt.show()

vars_c2018_1 = naf.community_description(c2018_1, var_class)
vars_c2018_1.to_csv(data_path + "/socialframeworkvariables/c2018_1.csv")

# Community 2-2018

c2018_2 = nx.subgraph(Network2018[0], C2018[0][1])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8.2 * 1.618, 8.2))
    ax.axis("off")
    nx.draw_networkx(
        c2018_2,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="orange",
        pos=nx.fruchterman_reingold_layout(c2018_2, seed=seed),
    )
plt.title("Comunidad 2")
plt.savefig("reports/figures/C2_2018.pdf", bbox_inches="tight")
plt.show()

vars_c2018_2 = naf.community_description(c2018_2, var_class)
vars_c2018_2.to_csv(data_path + "/socialframeworkvariables/c2018_2.csv")

# Community 3-2018

c2018_3 = nx.subgraph(Network2018[0], C2018[0][2])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2018_3,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="green",
        pos=nx.fruchterman_reingold_layout(c2018_3, seed=seed),
        font_size=9,
    )
plt.title("Comunidad 3")
plt.savefig("reports/figures/C3_2018.pdf", bbox_inches="tight")
plt.show()

vars_c2018_3 = naf.community_description(c2018_3, var_class)
vars_c2018_3.to_csv(data_path + "/socialframeworkvariables/c2018_3.csv")

# Community 4-2018

c2018_4 = nx.subgraph(Network2018[0], C2018[0][3])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2018_4,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="red",
        pos=nx.fruchterman_reingold_layout(c2018_4, seed=seed),
    )
plt.title("Comunidad 4")
plt.savefig("reports/figures/C4_2018.pdf", bbox_inches="tight")
plt.show()

vars_c2018_4 = naf.community_description(c2018_4, var_class)
vars_c2018_4.to_csv(data_path + "/socialframeworkvariables/c2018_4.csv")

# Community 1-2020

c2020_1 = nx.subgraph(Network2020[0], C2020[0][0])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2020_1,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="blue",
        pos=nx.fruchterman_reingold_layout(c2020_1, seed=seed),
    )
plt.title("Comunidad 1")
plt.savefig("reports/figures/C1_2020.pdf", bbox_inches="tight")
plt.show()

vars_c2020_1 = naf.community_description(c2020_1, var_class)
vars_c2020_1.to_csv(data_path + "/socialframeworkvariables/c2020_1.csv")

# Community 2-2020

c2020_2 = nx.subgraph(Network2020[0], C2020[0][1])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8.2 * 1.618, 8.2))
    ax.axis("off")
    nx.draw_networkx(
        c2020_2,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="orange",
        pos=nx.fruchterman_reingold_layout(c2020_2, seed=seed),
    )
plt.title("Comunidad 2")
plt.savefig("reports/figures/C2_2020.pdf", bbox_inches="tight")
plt.show()

vars_c2020_2 = naf.community_description(c2020_2, var_class)
vars_c2020_2.to_csv(data_path + "/socialframeworkvariables/c2020_2.csv")

# Community 3-2020

c2020_3 = nx.subgraph(Network2020[0], C2020[0][2])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8 * 1.618, 8))
    ax.axis("off")
    nx.draw_networkx(
        c2020_3,
        with_labels=True,
        node_size=300,
        alpha=1,
        edge_color="lightgray",
        node_color="green",
        pos=nx.fruchterman_reingold_layout(c2020_3, seed=seed),
        font_size=9,
    )
plt.title("Comunidad 3")
plt.savefig("reports/figures/C3_2020.pdf", bbox_inches="tight")
plt.show()

vars_c2020_3 = naf.community_description(c2020_3, var_class)
vars_c2020_3.to_csv(data_path + "/socialframeworkvariables/c2020_3.csv")

# Community 4-2020

c2020_4 = nx.subgraph(Network2020[0], C2020[0][3])
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(8.2 * 1.618, 8.2))
    ax.axis("off")
    nx.draw_networkx(
        c2020_4,
        with_labels=True,
        node_size=150,
        alpha=1,
        edge_color="lightgray",
        node_color="red",
        pos=nx.fruchterman_reingold_layout(c2020_4, seed=seed),
        font_size=9,
    )
plt.title("Comunidad 4")
plt.savefig("reports/figures/C4_2020.pdf", bbox_inches="tight")
plt.show()

vars_c2020_4 = naf.community_description(c2020_4, var_class)
vars_c2020_4.to_csv(data_path + "/socialframeworkvariables/c2020_4.csv")
