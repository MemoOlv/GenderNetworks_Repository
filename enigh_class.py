from functools import reduce
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
import pandas as pd


class Data(ABC):

    @abstractmethod
    def classification_age_generation(self):
        """Classification according age generation of members in household"""

    @abstractmethod
    def classification_sex_age(self):
        """Classification according sex household referent person and age of members"""

    @abstractmethod
    def clean_data(self):
        """Clean data with more than 10% of null values"""

    @abstractmethod
    def drop_nonessential_columns(self):
        """Removes non-essential columns for analysis""""

    @abstractmethod
    def read_data(self):
        """Return ENIGH dataframe"""

    @abstractmethod
    def read_tables(self):
        """Read tables from ENIGH database"""

    @abstractmethod
    def proportion_nan(self):
        """Compute proportion of missing values for variables in ENIGH dataset"""

    @abstractmethod
    def standarization(self):
        """Standarization of dataset"""

@dataclass
class ENIGH_Data(Data):
    """Class that contains ENIGH data for year"""


    year: int = 2016
    clean: bool = True
    type_class: str = "Sex_HHRP_Age"


    def classification_age_generation(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Classification according generation of members in household"""
        if self.year == 2016:
            generation = [dataset.edad<=16,
                          (dataset.edad>16) & (dataset.edad<=26),
                          (dataset.edad>26) & (dataset.edad<=36),
                          (dataset.edad>36) & (dataset.edad<=46),
                          (dataset.edad>46) & (dataset.edad<=56),
                          (dataset.edad>56) & (dataset.edad>=66)]
            choices = ["G_after_2000", "G_90s","G_80s","G_70s","G_60s","G_50s"]
            dataset["node"] = np.select(generation, choices, default="G_older_50s")
        elif self.year == 2018:
            generation = [dataset.edad<=18,
                          (dataset.edad>18) & (dataset.edad<=28),
                          (dataset.edad>28) & (dataset.edad<=38),
                          (dataset.edad>38) & (dataset.edad<=48),
                          (dataset.edad>48) & (dataset.edad<=58),
                          (dataset.edad>58) & (dataset.edad>=68)]
            choices = ["G_after_2000", "G_90s","G_80s","G_70s","G_60s","G_50s"]
            dataset["node"] = np.select(generation, choices, default="G_older_50s")
        elif self.year == 2020:
            generation = [dataset.edad<=20,
                          (dataset.edad>20) & (dataset.edad<=30),
                          (dataset.edad>30) & (dataset.edad<=40),
                          (dataset.edad>40) & (dataset.edad<=50),
                          (dataset.edad>50) & (dataset.edad<=60),
                          (dataset.edad>60) & (dataset.edad>=70)]
            choices = ["G_after_2000", "G_90s","G_80s","G_70s","G_60s","G_50s"]
            dataset["node"] = np.select(generation, choices, default="G_older_50s")
        return dataset


    def classification_sex_age(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Classification according sex of household referent person and age"""
        #Sex classification
        sexHHRP = [(dataset.sexo_jefe==1),
                  (dataset.sexo_jefe==2)]
        choices = ["H","M"]
        dataset["sex_hhrp"] = np.select(sexHHRP, choices, default="empty")

        #age classification
        hh_members = [
            (dataset.p12_64>0) & (dataset.p65mas==0) & (dataset.menores==0),
            (dataset.p12_64>0) & (dataset.p65mas==0) & (dataset.menores>0),
            (dataset.p12_64>0) & (dataset.p65mas>0) & (dataset.menores==0),
            (dataset.p12_64==0) & (dataset.p65mas>0) & (dataset.menores>0),
            (dataset.p12_64==0) & (dataset.p65mas>0) & (dataset.menores==0),
            (dataset.p12_64>0) & (dataset.p65mas>0) & (dataset.menores>0)]
        choices = ["1","2","3","4","5","6"]
        dataset["age"] = np.select(hh_members, choices, default="empty")
        dataset["node"] = dataset.sex_hhrp + dataset.age
        return dataset


    def clean_data(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Clean data with more than 10% if null values"""
        column_missing = list()
        for column in dataset.columns:
            proportion = np.mean(dataset[column].isnull())
            if (proportion>=0.1):
                column_missing = np.append(column_missing, column)
        dataset.drop(columns=list(column_missing),inplace=True)
        dataset = dataset.dropna()
        return dataset


    def drop_nonessential_columns(self,dataset_merged):
        """Remove nonessential columns"""
        dataset_merged.drop(columns=["foliohog_x",
                                    "foliohog_y",
                                    "ubica_geo_y",
                                    "tam_loc_y",
                                    "est_socio_y",
                                    "est_dis_x",
                                    "est_dis_y",
                                    "upm_x",
                                    "upm_y",
                                    "factor_x",
                                    "factor_y",
                                    "smg",
                                    "numren",
                                    "foliohog"], inplace=True)
        if self.year<2018:
            dataset_merged.drop(columns=["ageb_x",
                                        "ageb_y"], inplace=True)

        dataset_merged.rename(columns={"ubica_geo_x":"ubica_geo",
                                      "tam_loc_x":"tam_loc",
                                      "est_socio_x":"est_socio"}, inplace=True)
        return dataset_merged


    def read_data(self) -> pd.DataFrame:
        """Reads data and merge into a single dataframe"""
        hogar = self.read_tables("hogares.csv", self.year)
        poblacion = self.read_tables("poblacion.csv",self.year)
        concentrado = self.read_tables("concentradohogar.csv",self.year)
        viviendas = self.read_tables("viviendas.csv",self.year)

        datasets_list = [hogar, poblacion, concentrado, viviendas]

        dataset_merged = reduce(lambda left, right: pd.merge(left, right, on="folioviv", how="outer"),
                               datasets_list)

        dataset_merged = self.drop_nonessential_columns(dataset_merged)


        if self.clean:
            return self.clean_data(dataset_merged)
        else:
            return dataset_merged


    def read_tables(self,table_name,year) -> pd.DataFrame:
        """Reads data from tables of ENIGH """
        data_path = "../Data/ENIGH" + str(year) + "/"
        dataset = pd.read_csv(data_path+table_name,
                             index_col="folioviv",
                             low_memory=False,
                             na_values=[" ", "&"])
        return dataset


    def proportion_nan(self, dataset: pd.DataFrame):
        """Compute proportion of missing values from ENIGH dataset"""
        proportion_list = list()
        for column in dataset.columns:
            proportion = np.mean(dataset[column].isnull())
            proportion_list = np.append(proportion_list, proportion)
        return proportion_list


    def standardization(self) -> pd.DataFrame:
        """Standardization of dataset"""
        dataset_standardized = self.classification().copy()
        for column in dataset_standardized.columns[:-1]:
            if (dataset_standardized[column].std(ddof=0)==0):
                dataset_standardized.drop(columns=column, inplace=True)
            else:
                dataset_standardized[column] = (dataset_standardized[column] - dataset_standardized[column].mean())/dataset_standardized[column].std()
        return dataset_standardized
