import numpy as np
import pandas as pd
from functools import reduce


def get_enigh_2016_dataframe(year, data_path):
    path_name = data_path + "ENIGH" + year + "/"
    enigh_dataframes = get_enigh_tables(path_name)
    enigh_dataframe_merged = merge_data(enigh_dataframes)
    enigh_dataframe_merged.drop(columns=list_columns_to_drop_enigh_2016,inplace=True,)
    enigh_dataframe_merged.rename(columns=columns_to_rename,inplace=True,)
    return enigh_dataframe_merged

def get_enigh_2018_and_2020_dataframe(year, data_path):
    path_name = data_path + "ENIGH" + year + "/"
    enigh_dataframes = get_enigh_tables(path_name)
    enigh_dataframe_merged = merge_data(enigh_dataframes)
    enigh_dataframe_merged.drop(columns=list_columns_to_drop_enigh_2018_and_2020,inplace=True,)
    enigh_dataframe_merged.rename(columns=columns_to_rename,inplace=True,)
    return enigh_dataframe_merged

def get_enigh_tables(path):
    hogares_dataframe = read_tables(path + "hogares.csv")
    poblacion_dataframe = read_tables(path + "poblacion.csv")
    concentrado_dataframe = read_tables(path + "concentradohogar.csv")
    vivienda_dataframe = read_tables(path + "viviendas.csv")
    enigh_dataframes = [
        poblacion_dataframe,
        hogares_dataframe,
        concentrado_dataframe,
        vivienda_dataframe,
    ]
    return(enigh_dataframes)

list_columns_to_drop_enigh_2016 = [
    "ageb_x",
    "ageb_y",
    "est_dis_x",
    "est_dis_y",
    "est_socio_y",
    "factor_x",
    "factor_y",
    "foliohog_x",
    "foliohog_y",
    "numren",
    "smg",
    "tam_loc_y",
    "ubica_geo_y",
    "upm_x",
    "upm_y",
    ]

list_columns_to_drop_enigh_2018_and_2020 = [
    "est_dis_x",
    "est_dis_y",
    "est_socio_y",
    "factor_x",
    "factor_y",
    "foliohog_x",
    "foliohog_y",
    "foliohog",
    "numren",
    "smg",
    "tam_loc_y",
    "ubica_geo_y",
    "upm_x",
    "upm_y",
    ]

columns_to_rename = {
    "ubica_geo_x": "ubica_geo",
    "tam_loc_x": "tam_loc",
    "est_socio_x": "est_socio",}

def read_tables(data_path):
    return pd.read_csv(data_path, index_col="folioviv", na_values=["&", " "])


def merge_data(list_of_dataframes):
    return reduce(lambda left, right: pd.merge(left, right, on="folioviv", how="outer"), list_of_dataframes)