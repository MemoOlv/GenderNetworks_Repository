import pandas as pd

from gender_energy_networks import get_enigh_dataframe


class ENIGH_database():
    """Python class to process ENIGH database""" 
    year: int = 0

    def set_year(self, year):
        self.year = year

    def read_data(self) -> pd.DataFrame:
        enigh_dataframe = get_enigh_dataframe(self.year)
        return(enigh_dataframe)


