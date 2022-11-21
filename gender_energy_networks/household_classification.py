import numpy as np

def hhld_classification(df):
    # Classification by sex of household referent person
    sexHHRP = [(df.sexo_jefe == 1), (df.sexo_jefe == 2)]
    choices = ["H", "M"]
    df["sex_hhrp"] = np.select(sexHHRP, choices, default="empty")

    # Classification by age range of household members
    hh_members = [
        (df.p12_64 > 0) & (df.p65mas == 0) & (df.menores == 0),
        (df.p12_64 > 0) & (df.p65mas == 0) & (df.menores > 0),
        (df.p12_64 > 0) & (df.p65mas > 0) & (df.menores == 0),
        (df.p12_64 == 0) & (df.p65mas > 0) & (df.menores > 0),
        (df.p12_64 == 0) & (df.p65mas > 0) & (df.menores == 0),
        (df.p12_64 > 0) & (df.p65mas > 0) & (df.menores > 0),
    ]

    choices = [
        "Adultos",
        "AdultosMenores",
        "AdultosMayores",
        "MayoresMenores",
        "Mayores",
        "AdultosMayoresMenores",
    ]
    df["age_habit"] = np.select(hh_members, choices, default="empty")
    df["node"] = df.sex_hhrp + df.age_habit

    return df