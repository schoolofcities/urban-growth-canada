
# this script gets a list of every CSD in the Greater Golden Horseshoe with their respective CD and CMA

import pandas as pd
import zipfile

# prior to running, downloaded the Geographic Relationships File and saved it locally (only ~2mb)
# https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/dguid-idugd/index2021-eng.cfm?year=21

# load data from zip
zf = zipfile.ZipFile('2021_98260004.zip') 
df = pd.read_csv(zf.open('2021_98260004.csv'))
print(df)

# these are the three columns we want
# CD - "CDDGUID_DRIDUGD" - last 4 digits
# CSD - "CSDDGUID_SDRIDUGD" - last 7 digits
# CMA - "CMADGUID_RMRIDUGD" - last 3 digits

# generating ID columns
df = df[["CDDGUID_DRIDUGD", "CSDDGUID_SDRIDUGD", "CMADGUID_RMRIDUGD"]]
df["CDUID"] = df["CDDGUID_DRIDUGD"].str[-4:]
df["CSDUID"] = df["CSDDGUID_SDRIDUGD"].str[-7:]
df["CMAUID"] = df["CMADGUID_RMRIDUGD"].str[-3:]

# list of the CDs in the Greater Golden Horseshoe
ggh = ["3543","3523","3516","3515","3514","3518","3519","3520","3521","3524","3530","3525","3529","3526","3528"]

# filtering by CD list 
df = df[df["CDUID"].isin(ggh)]

# dropping duplicates and sorting
df = df.drop_duplicates()
df = df.sort_values("CSDUID")

# save to file
df.to_csv("ggh-csd-cd-cma.csv", index = None)
