import pandas as pd
import zipfile

# 1996 Data to 2021 CTs

# the apportionment table
crosswalk_csv = 'ct_1996_2021_link.csv'

# the csv with source tract data to apportioned
data_csv = 'ct_1996_data.csv'

# read in the data
df = pd.read_csv(data_csv, dtype = {"ctuid": str, "pop_1996": float, "dwe_1996": float})


# names of columns we want ot apportion
fields = [
    ["pop_1996","w_pop", None],
    ["dwe_1996","w_dwe", None]
]

# read in crosswalk table
cw = pd.read_csv(crosswalk_csv, dtype = {"source_ctuid": str, "target_ctuid": str})

# joining the two input tables
merge_cw_df = cw.merge(df, how = "inner", left_on = "source_ctuid", right_on = "ctuid")

print(merge_cw_df)

# loop over each field, multiplying by the apportionment weight
output_fields = []
for f in fields:
	name = f[0]
	weight = f[1]
	mult = f[2]
	print(f)

	merge_cw_df[name + "_" + weight] = merge_cw_df[weight] * merge_cw_df[name]
	output_fields.append(name + "_" + weight)


print(merge_cw_df)

	
# group by the target census tracts, summing by the wanted fields
df_96_in_21 = merge_cw_df.groupby(["target_ctuid"]).sum()
df_96_in_21 = df_96_in_21[output_fields]

for f in fields:
	name = f[0]
	weight = f[1]
	mult = f[2]
	if mult is not None:
		df_96_in_21[name + "_" + weight] = df_96_in_21[name + "_" + weight] / df_96_in_21[mult + "_" + weight]

df_96_in_21["pop96"] = df_96_in_21["pop_1996_w_pop"].astype(int)
del df_96_in_21["pop_1996_w_pop"]

df_96_in_21["dwe96"] = df_96_in_21["dwe_1996_w_dwe"].astype(int)
del df_96_in_21["dwe_1996_w_dwe"]

df_96_in_21.to_csv("ct_2021_with_1996_data.csv")
