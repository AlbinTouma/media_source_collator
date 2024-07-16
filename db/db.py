import os
import pandas as pd
import glob

path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))

df = pd.DataFrame()
for f in csv_files:
    x = pd.read_csv(f)
    df = pd.concat([x], axis=0)

df = df[['name','domain', 'provider', 'owners', 'frequency', 'web_site_id', 'created_date', 'updated_date', 'country', 'lat', 'lng']]
print(df['country'])
