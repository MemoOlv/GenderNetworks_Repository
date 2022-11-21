import hashlib

def test_plot_null_values():
    expected_hash = "abc"
    file_path = "tests/figures/plot_null_values_2016.pdf"
    plot_null_values(file_path)
    obtained_hash = get_hash_from_file(file_path)
    assert obtained_hash == expected_hash


def get_hash_from_file(file_path):
    encoded_string = file_path.enconde("utf-8")
    return hashlib.md5(encoded_string).hexdigest()
