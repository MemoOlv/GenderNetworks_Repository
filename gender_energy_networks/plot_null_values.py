import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_null_values(enigh_dataframe, file_path):
    sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})
    
    percentage_missing = _get_percentage_missing(enigh_dataframe)
    
    f = plt.figure(figsize=(10, 6))
    f.subplots_adjust(hspace=0.2)
    fontsize_ticks = 20
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])
    ax.tick_params(labelsize=fontsize_ticks)
    sns.despine()
    sns.histplot(percentage_missing, kde=False)
    plt.xlabel("$n_{i}$", fontsize=fontsize_ticks)
    plt.ylabel("Frecuencia", fontsize=fontsize_ticks)
    plt.savefig(file_path, bbox_inches="tight")

def _get_percentage_missing(enigh_dataframe):
    return [np.mean(enigh_dataframe[col].isnull()) for col in enigh_dataframe.columns]
    