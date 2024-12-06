import pandas as pd

def statistics_df(df: pd.DataFrame()):
    return df.describe(percentiles=[0.1,0.3,0.6])


