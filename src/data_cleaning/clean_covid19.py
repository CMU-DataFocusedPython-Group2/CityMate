# Author: Jingwen Ma, Yixuan Guo, Yue Jia, Yunxuan Yu, Zixin Yin
# Date: Oct-11, 2020

# pip install sodapy
# pip install shapely
# if you are python 3.8, you may need to copy the geo_c dlls into library\bin
import pandas as pd
import requests,io
from sodapy import Socrata
from shapely.geometry import Point, Polygon

client = Socrata("data.cityofnewyork.us", 'weom0t1xmEmSCKQihBJ7FJ4kT')
results = client.get("pri4-ifjk", limit=2000)
results_df = pd.DataFrame.from_records(results)
modzcta_df = results_df.drop(['label','zcta','pop_est'],axis=1).set_index('modzcta',drop=True)

# convert longitute-latitude to ZCTA code to match COVID-19 data
def LngLat_to_ZCTA(Lng,Lat):
    p1 = Point(Lng,Lat)
    i = 0
    while(i<=len(modzcta_df.index)-1):
        poly = Polygon(modzcta_df.iloc[i].the_geom['coordinates'][0][0])
        if(p1.within(poly)):
            return modzcta_df.iloc[i].name
        else:
            i += 1
    i = 0
    while(i<=len(modzcta_df.index)-1):
        poly = Polygon(modzcta_df.iloc[i].the_geom['coordinates'][0][0])
        dis = poly.centroid.distance(p1)
        if i==0:
            min_dis = dis
            name = modzcta_df.iloc[i].name
        elif dis < min_dis:
            min_dis = dis
            name = modzcta_df.iloc[i].name
        i += 1
    return(name)


# GET COVID_DATA
# GET COVID_DATA
def GET_COVID19_DF():
    url= "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/recent/recent-4-week-by-modzcta.csv"
    s= requests.get(url).content
    rawdata = pd.read_csv(io.StringIO(s.decode('utf-8')))
    rawdata.rename(columns={'MODIFIED_ZCTA': 'ZCTA'}, inplace=True)
    covidlist = []
    for row in rawdata.iterrows():
        data = row[1]
        item = []
        item.append(data.ZCTA)
        item.append(data.NEIGHBORHOOD_NAME)
        item.append(data.COVID_CASE_COUNT_4WEEK)
        item.append(data.COVID_CASE_RATE_4WEEK)
        item.append(data.COVID_DEATH_COUNT_4WEEK)
        item.append(data.COVID_DEATH_RATE_4WEEK)
        item.append(data.NUM_PEOP_TEST_4WEEK)
        item.append(data.PERCENT_POSITIVE_4WEEK)
        item.append([data.COVID_CASE_COUNT_WEEK1,data.COVID_CASE_COUNT_WEEK2,data.COVID_CASE_COUNT_WEEK3,data.COVID_CASE_COUNT_WEEK4])
        covidlist.append(item)
    COVID_DATA = pd.DataFrame(covidlist)
    COVID_DATA.columns = ['ZCTA','NEIGHBORHOOD_NAME','COVID_CASE_COUNT_4WEEK','COVID_CASE_RATE_4WEEK','COVID_DEATH_COUNT_4WEEK',
                         'COVID_DEATH_RATE_4WEEK','NUM_PEOP_TEST_4WEEK','PERCENT_POSITIVE_4WEEK','CASE_COUNT_CHANGE_4WEEK']
    return COVID_DATA

if __name__ == "__main__":
    COVID_DATA = GET_COVID19_DF()
    COVID_DATA.to_csv('../../data/updated_data/covid19_clean.csv', index=False)
