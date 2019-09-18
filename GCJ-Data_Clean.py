import pandas as pd
import numpy as np

filename = 'GCJ_Epic_Survey_2019.csv'
col_names = ['Timestamp CET', 'Age', 'Gender', 'Region', 'Ethnicity', 'Platforms Owned', 'Platforms May', 'Fav Pubs', 'Fav Devs', 'Fav Franchises', 'Data Sales']

# produce the dataframe from the CSV, replacing the column names with the list in col_names
df = pd.read_csv(filename, header=0, names=col_names, parse_dates=[0])

print(df.head())
print(df.iloc[0,0])
print(type(df.iloc[0,0]))

# write the cleaned .csv for other tasks to work on
_ = df.to_csv('GCJ_Data-Cleaned.csv', index=False)
