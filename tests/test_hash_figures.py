import hashlib

from gender_energy_networks import plot_null_values

def test_plot_null_values():
    expected_hash = "5c3642e40c73bc1d0363a68322aef26a"
    file_path = "tests/figures/plot_null_values_2016.pdf"
    plot_null_values(file_path)
    obtained_hash = get_hash_from_file(file_path)
    assert obtained_hash == expected_hash


def get_hash_from_file(file_path):
    encoded_string = hashlib.md5(file_path.encode("utf-8"))
    return encoded_string.hexdigest()
