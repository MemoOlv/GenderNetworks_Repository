import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_null_values(file_path):
    sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})
    ENIGHr = pd.read_csv("data/ENIGH2016_dataframe.csv")
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
    plt.savefig(file_path, bbox_inches="tight")
