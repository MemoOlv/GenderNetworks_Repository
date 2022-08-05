from gender_energy_networks import ENIGH_database

def test_ENIGH_database_set_year():
    expected_year_of_analisys = 2016
    ENIGH = ENIGH_database()
    ENIGH.set_year(expected_year_of_analisys)
    obtained_year_of_analisys = ENIGH.year
    assert expected_year_of_analisys == obtained_year_of_analisys