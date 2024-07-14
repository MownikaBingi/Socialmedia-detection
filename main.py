import pandas as pd

df = pd.read_csv('twitter_data.csv')
user_id = '7'
print(df.iloc[7].to_dict())
