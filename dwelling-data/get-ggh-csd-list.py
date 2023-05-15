import pandas as pd
import zipfile

zf = zipfile.ZipFile('2021_98260004.zip') 
df = pd.read_csv(zf.open('2021_98260004.csv'))

print(df)
