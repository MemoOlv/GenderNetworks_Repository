from condor import condor_object

from gender_energy_networks import ENIGH_database

def test_ENIGH_database_set_year():
    expected_year_of_analisys = 2016
    ENIGH = ENIGH_database()
    ENIGH.set_year(expected_year_of_analisys)
    obtained_year_of_analisys = ENIGH.year
    assert expected_year_of_analisys == obtained_year_of_analisys

def test_condor_installation():
    class ThisClass: pass
    obtained_condor_object_type = type(condor_object)
    expected_condor_object_type = type(ThisClass)
    assert obtained_condor_object_type == expected_condor_object_type
