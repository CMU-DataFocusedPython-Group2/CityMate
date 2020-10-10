import pandas as pd
import requests

def GET_RESTAURANT_DF():
    r = requests.get("https://data.cityofnewyork.us/api/views/59dk-tdhz/rows.csv?accessType=DOWNLOAD", stream=True)
    f = open("restaurant.csv", "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    res_df = pd.DataFrame()
    rawdata = pd.read_csv("restaurant_point.csv").dropna(subset=['cuisine','name','addr:street','phone'])
    res_df['Lng'] = rawdata[rawdata.columns[0]]
    res_df['Lat'] = rawdata[rawdata.columns[1]]
    res_df['name'] = rawdata.name
    res_df['cuisine'] = rawdata.cuisine
    res_df['street'] = rawdata['addr:street']
    res_df['phone'] = rawdata.phone
    return res_df

if __name__ == "__main__":
    res_df = GET_RESTAURANT_DF()
    res_df.to_csv('Restaurant_clean.csv', index = False)