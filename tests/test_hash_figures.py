import hashlib
import pandas as pd

from gender_energy_networks import plot_null_values


def test_plot_null_values():
    enigh_dataframe = pd.read_csv("tests/data/input_plot_null_values.csv")
    file_path = "tests/data/plot_null_values.png"
    plot_null_values(enigh_dataframe, file_path)
    obtained_hash = _get_hash_from_file(file_path)
    expected_hash = "0684c592f94501ee3e1d8f1e4bd9c6f5"
    assert obtained_hash == expected_hash


def _get_hash_from_file(file_path):
    file_content = open(file_path, "rb").read()
    file_hash = hashlib.md5(file_content).hexdigest()
    return file_hash
