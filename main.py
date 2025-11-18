# Educational project

import pandas as pd

# url = "https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv"
url = "data/uk-500.csv"
df = pd.read_csv(url)
print(df.head())

df.head()
df.info()
df.describe()
