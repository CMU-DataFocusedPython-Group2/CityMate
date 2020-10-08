import pandas as pd

res_df = pd.DataFrame()
rawdata = pd.read_csv("restaurant_point.csv").dropna(subset=['cuisine','name','addr:street','phone'])
res_df['Lng'] = rawdata[rawdata.columns[0]]
res_df['Lat'] = rawdata[rawdata.columns[1]]
res_df['name'] = rawdata.name
res_df['cuisine'] = rawdata.cuisine
res_df['street'] = rawdata['addr:street']
res_df['phone'] = rawdata.phone
res_df.to_csv('Restaurant_clean.csv', index = False)