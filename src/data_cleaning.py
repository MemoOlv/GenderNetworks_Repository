import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
import data_processing_functions as dpf


sys_path = "/home/perroloco/Escritorio/GenderNetworks_Repository"
lib_path = "/lib"
sys.path.insert(0, sys_path + lib_path)
sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})

data_path = sys_path + "/data/"
yr = "2020"  # choices are 2016, 2018 and 2020

ENIGHr = dpf.read_data(yr, data_path)
ENIGH = ENIGHr.copy()

pct_missing = []
col_missing = []
pct_col = []
for col in ENIGH.columns:
    pct = np.mean(ENIGH[col].isnull())
    pct_missing = np.append(pct_missing, pct)
    pct_col.append(str(col) + "->" + str(pct) + "%")
    if pct >= 0.1:
        col_missing = np.append(col_missing, col)

f = plt.figure(figsize=(10, 6))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.histplot(pct_missing, kde=False)
plt.xlabel("$n_{i}$", fontsize=fontsize_ticks)
plt.ylabel("Frecuencia", fontsize=fontsize_ticks)
plt.savefig(sys_path + "/figures/ValoresNulos" + yr + ".pdf", bbox_inches="tight")
plt.show()

ENIGH.drop(columns=list(col_missing), inplace=True)

pct_missing = []
col_missing = []
for col in ENIGH.columns:
    pct = np.mean(ENIGH[col].isnull())
    pct_missing = np.append(pct_missing, pct)
    if pct >= 0.1:
        col_missing = np.append(col_missing, col)

f = plt.figure(figsize=(10, 6))
f.subplots_adjust(hspace=0.2)
fontsize_ticks = 20
gs = gridspec.GridSpec(1, 1)
ax = plt.subplot(gs[0])
ax.tick_params(labelsize=fontsize_ticks)
sns.despine()
sns.histplot(pct_missing, kde=False)
plt.xlabel("$n_{i}$", fontsize=fontsize_ticks)
plt.ylabel("Frecuencia", fontsize=fontsize_ticks)
plt.savefig(sys_path + "/figures/ValoresNuloRemoval" + yr + ".pdf", bbox_inches="tight")
plt.show()

ENIGH = ENIGH.dropna()
ENIGH.to_csv(data_path + "ENIGH" + yr + "_clean.csv")
