import numpy as np
import pandas as pd
from functools import reduce
import seaborn as sns
from scipy.stats import multivariate_normal
import csv


def read_tables(data_path):
    return pd.DataFrame(data = {"a": [1, 2], "b": [3, 4]})

def read_data(year, data_path):
    path_name = data_path + "ENIGH" + year + "/"
    hog = pd.read_csv(
        path_name + "hogares.csv", index_col="folioviv", low_memory=False, na_values=[" ", "&"]
    )
    pob = pd.read_csv(
        path_name + "poblacion.csv", index_col="folioviv", low_memory=False, na_values=[" ", "&"]
    )
    conc = pd.read_csv(
        path_name + "concentradohogar.csv",
        index_col="folioviv",
        low_memory=False,
        na_values=[" ", "&"],
    )
    viv = pd.read_csv(
        path_name + "viviendas.csv", index_col="folioviv", low_memory=False, na_values=[" ", "&"]
    )
    data_frames = [pob, hog, conc, viv]

    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on="folioviv", how="outer"), data_frames
    )
    if int(year) >= 2018:
        df_merged.drop(
            columns=[
                "foliohog_x",
                "foliohog_y",
                "ubica_geo_y",
                "tam_loc_y",
                "est_socio_y",
                "est_dis_y",
                "upm_y",
                "factor_y",
                "smg",
                "est_dis_x",
                "upm_x",
                "factor_x",
                "numren",
                "foliohog",
            ],
            inplace=True,
        )
        df_merged.rename(
            columns={
                "ubica_geo_x": "ubica_geo",
                "tam_loc_x": "tam_loc",
                "est_socio_x": "est_socio",
            },
            inplace=True,
        )
    elif int(year) == 2016:
        df_merged.drop(
            columns=[
                "foliohog_x",
                "foliohog_y",
                "ubica_geo_y",
                "tam_loc_y",
                "est_socio_y",
                "est_dis_y",
                "upm_y",
                "factor_y",
                "smg",
                "ageb_y",
                "ageb_x",
                "est_dis_x",
                "upm_x",
                "factor_x",
                "numren",
            ],
            inplace=True,
        )
        df_merged.rename(
            columns={
                "ubica_geo_x": "ubica_geo",
                "tam_loc_x": "tam_loc",
                "est_socio_x": "est_socio",
            },
            inplace=True,
        )
    return df_merged


def strg(variable):
    var = variable.astype(int).apply(str)
    return var


def standardization(df):
    df_std = df.copy()
    for column in df_std.columns[:-2]:
        if df_std[column].std(ddof=0) == 0:
            df_std.drop(columns=column, inplace=True)
        else:
            df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()
    return df_std


def hhld_classification(df):
    # Classification by sex of household referent person
    sexHHRP = [(df.sexo_jefe == 1), (df.sexo_jefe == 2)]
    choices = ["H", "M"]
    df["sex_hhrp"] = np.select(sexHHRP, choices, default="empty")

    # Classification by age range of household members
    hh_members = [
        (df.p12_64 > 0) & (df.p65mas == 0) & (df.menores == 0),
        (df.p12_64 > 0) & (df.p65mas == 0) & (df.menores > 0),
        (df.p12_64 > 0) & (df.p65mas > 0) & (df.menores == 0),
        (df.p12_64 == 0) & (df.p65mas > 0) & (df.menores > 0),
        (df.p12_64 == 0) & (df.p65mas > 0) & (df.menores == 0),
        (df.p12_64 > 0) & (df.p65mas > 0) & (df.menores > 0),
    ]

    choices = [
        "Adultos",
        "AdultosMenores",
        "AdultosMayores",
        "MayoresMenores",
        "Mayores",
        "AdultosMayoresMenores",
    ]
    df["age_habit"] = np.select(hh_members, choices, default="empty")
    df["node"] = df.sex_hhrp + df.age_habit

    return df

    # Fibonacci series to apply into the powerlaw visualization


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
