import pandas as pd
import numpy as np
from gender_energy_networks import read_data, read_tables, merge_data


def test_read_data():
    read_data()
    pass


def test_read_tables():
    hogar_path = "tests/data/hogares_data.csv"
    obtained_output = read_tables(hogar_path)
    expected_output = pd.DataFrame(
        data={"folioviv": [100003801, 100003802], "foliohog": [np.nan, np.nan], "huespedes": [0, 0]}
    )
    expected_output.set_index("folioviv", inplace=True)
    pd.testing.assert_frame_equal(obtained_output, expected_output)


def test_merge_data():
    dataframe_one = pd.DataFrame(data={"a": [1, 2], "b": [3, 4]})
    dataframe_two = pd.DataFrame(data={"a": [1, 2], "c": [3, 4], "b": [5, 6]})
    expected_merged_dataframe = merge_data(dataframe_one, dataframe_two)
    obtained_merged_dataframe = pd.DataFrame(
        data={
            "a_x": [1.0, 2.0, np.nan, np.nan],
            "b": [3, 4, 5, 6],
            "a_y": [np.nan, np.nan, 1.0, 2.0],
            "c": [np.nan, np.nan, 3.0, 4.0],
        }
    )
    pd.testing.assert_frame_equal(obtained_merged_dataframe, expected_merged_dataframe)
