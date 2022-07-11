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
    merge_data()
