'''import requests
import json
import pandas as pd
import numpy as np
import xlwt
import zipfile
import io
import time
from sodapy import Socrata
from shapely.geometry import Point, Polygon
from bs4 import BeautifulSoup'''
from clean_crime import GET_CRIME_DF
from clean_stops import GET_STOPS_DF

def UPDATE_DATA():
    CRIME_DF = GET_CRIME_DF()
    print(CRIME_DF)
    SUBSTOPS_DF = GET_STOPS_DF()
    print(SUBSTOPS_DF)
    '''RESTAURANT_DF = GET_RESTAURANT_DF()
    print(RESTAURANT_DF)
    THEATER_DF = GET_THEATRE_DF()
    print(THEATER_DF)'''
    return

'''def UPDATE_HOUSE_DATA():
    HOUSE_DF = GET_HOUSE_DF()
    print(HOUSE_DF)
    return

client = Socrata("data.cityofnewyork.us", 'weom0t1xmEmSCKQihBJ7FJ4kT')
results = client.get("pri4-ifjk", limit=2000)
results_df = pd.DataFrame.from_records(results)
modzcta_df = results_df.drop(['label','zcta','pop_est'],axis=1).set_index('modzcta',drop=True)

# function that convert longitute-latitude to ZCTA code
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
    return(name)'''

if __name__ == "__main__":
    UPDATE_DATA()