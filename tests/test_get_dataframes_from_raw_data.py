import pandas as pd
import numpy as np
from gender_energy_networks import (
    read_tables,
    merge_data,
    get_enigh_dataframe,
    ENIGH_database,
)


def test_enigh_database_read_data_2016():
    year = 2016
    ENIGH = ENIGH_database()
    ENIGH.set_year(year)
    ENIGH2016_dataframe = ENIGH.read_data()
    obtained_length = len(ENIGH2016_dataframe)
    expected_length = 285569
    assert obtained_length == expected_length
    obtained_columns_length = len(ENIGH2016_dataframe.columns)
    expected_columns_length = 489
    assert obtained_columns_length == expected_columns_length


def test_get_enigh_dataframe_2018():
    year = "2018"
    ENIGH2018 = get_enigh_dataframe(year)
    obtained_length = len(ENIGH2018)
    expected_length = 299746
    assert obtained_length == expected_length
    obtained_columns_length = len(ENIGH2018.columns)
    expected_columns_length = 488
    assert obtained_columns_length == expected_columns_length


def test_read_tables():
    example_path = "tests/data/example_data.csv"
    obtained_output = read_tables(example_path)
    expected_output = pd.DataFrame(
        data={"folioviv": [100003801, 100003802], "foliohog": [np.nan, np.nan], "huespedes": [0, 0]}
    )
    expected_output.set_index("folioviv", inplace=True)
    pd.testing.assert_frame_equal(obtained_output, expected_output)

    expected_output = pd.DataFrame(
        data={"folioviv": [100003801, 100003802], "foliohog": [np.nan, np.nan], "huespedes": [0, 0]}
    )


def test_merge_data():
    hogar_path = "tests/data/hogares_data.csv"
    concentrado_path = "tests/data/concentrado_data.csv"

    hogares_dataframe = read_tables(hogar_path)
    concentrado_dataframe = read_tables(concentrado_path)

    list_of_dataframes = [hogares_dataframe, concentrado_dataframe]

    expected_merged_dataframe = merge_data(list_of_dataframes)
    obtained_merged_dataframe = pd.DataFrame(
        data={
            "folioviv": [100003801, 100003801],
            "foliohog_x": [1, 1],
            "acc_alim1": [1, 2],
            "foliohog_y": [1, 1],
            "edad_jefe": [33, 29],
        }
    )
    obtained_merged_dataframe.set_index("folioviv", inplace=True)
    pd.testing.assert_frame_equal(obtained_merged_dataframe, expected_merged_dataframe)
