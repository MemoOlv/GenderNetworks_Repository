import hashlib
import pandas as pd

from gender_energy_networks import plot_null_values

def test_plot_null_values():
    expected_hash = "b28049c4937aad50ba339b17dc7691be"
    file_path = "tests/figures/plot_null_values_2016.pdf"
    enigh_dataframe = pd.read_csv("data/ENIGH2016_dataframe.csv")
    plot_null_values(enigh_dataframe, file_path)
    obtained_hash = get_hash_from_file(file_path)
    assert obtained_hash == expected_hash


def get_hash_from_file(file_path):
    encoded_string = hashlib.md5(file_path.encode("utf-8"))
    return encoded_string.hexdigest()
