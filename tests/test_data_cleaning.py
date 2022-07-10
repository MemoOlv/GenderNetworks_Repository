import pandas as pd
from gender_energy_networks import read_data, read_tables


def test_read_data():
    read_data()
    pass


def test_read_tables():
    obtained_output = read_tables()
    expected_output = pd.DataFrame(data = {"a": [1, 2], "b": [3, 4]})
    pd.testing.assert_frame_equal(obtained_output, expected_output)
    