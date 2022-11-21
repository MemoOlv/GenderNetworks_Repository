import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import gender_energy_networks as dpf


def plot_covmatrix_heatmap(enigh_dataframe, file_path):
    sns.set_style("whitegrid", {"grid.linestyle": "--", "axes.edgecolor": "0"})

    ENIGH =enigh_dataframe

    ENIGH = dpf.hhld_classification(ENIGH)

    ps_list = ENIGH.node.unique()
    ENIGH["count_node"] = ENIGH.groupby("node")["node"].transform("count")
    d = ENIGH.sort_values(by=["count_node"], ignore_index=True)

    ENIGH.drop(columns=["sex_hhrp", "age_habit"], inplace=True)

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
    plt.savefig(file_path, bbox_inches="tight")

