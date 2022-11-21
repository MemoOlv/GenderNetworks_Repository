import numpy as np
import pandas as pd


def strg(variable):
    var = variable.astype(int).apply(str)
    return var


def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return recur_fibo(n - 1) + recur_fibo(n - 2)


def criteria(dic, pc, n_nodes):
    df = dic[pc]
    df["covmul"] = df[pc] * df["cov"]

    c = df[df.index == df["covmul"].idxmax()]
    c = c[["idx", pc]]
    c["num"] = n_nodes[pc]
    c["PC"] = pc
    c.rename(columns={pc: "value"}, inplace=True)
    return [c, df]


def ComputeRepresentativity(df, type_class, yr, path):
    # Read ENIGH covariance matrix
    cov_matrixr = pd.read_csv(path + "cov_matrix_" + type_class + yr + ".csv", index_col=[0])
    cov_matrix = cov_matrixr.copy()
    keys = list(cov_matrix.columns.unique())

    representativity = {}
    n_nodes = {}
    for ps in keys:
        rep = (cov_matrix[ps] / sum(cov_matrix[ps])).sort_values(ascending=False).cumsum()
        representativity[ps] = rep
        representativity[ps] = representativity[ps].to_frame()
        representativity[ps]["idx"] = range(1, len(representativity[ps]) + 1)
        representativity[ps]["cov"] = cov_matrix[ps]
        n_nodes[ps] = len(df[df.node == ps])

    return (cov_matrix, keys, representativity, n_nodes)


def typeofcriteria(keys, criteriatype, frames1, mean, crt):
    frames = frames1
    m = mean
    crt = crt

    ps_n = list()
    cov_cut = {}
    for ps in keys:
        if criteriatype == "static":
            df_c = frames[ps][frames[ps][ps] <= m]  # Static criteria
        elif criteriatype == "dynamic":
            df_c = frames[ps][
                frames[ps][ps] <= np.array(crt[crt.PC == ps].value)[0]
            ]  # dynamic criteria
        df = df_c.copy()
        df.drop(index=list(df[df["cov"] == 0].index), inplace=True)
        if len(df) != 0:
            cov_cut[ps] = df["cov"]
            ps_n.append(ps)

        series_cut = list()  # List to recreate the covariance matrix after criteria analysis
        for ps in ps_n:
            sx = cov_cut[ps]
            sx.rename(ps, inplace=True)
            series_cut.append(sx)

    cov_matrix_cut = pd.concat(series_cut, axis=1).fillna(0)
    return cov_matrix_cut
