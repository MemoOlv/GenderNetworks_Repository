def standardization(df):
    df_std = df.copy()
    for column in df_std.columns[:-2]:
        if df_std[column].std(ddof=0) == 0:
            df_std.drop(columns=column, inplace=True)
        else:
            df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()
    return df_std
    