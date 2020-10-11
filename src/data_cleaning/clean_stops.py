#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import requests, zipfile, io
import numpy as np
import pandas as pd

def GET_STOPS_RAW():
    r = requests.get('http://web.mta.info/developers/data/nyct/subway/google_transit.zip')
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path = '../../data/raw_data/')

def CLEAN_STOPSDATA():
    path = '../../data/raw_data/stops.txt'
    with open(path) as f:
        lists = [i[:-1].split(',') for i in f.readlines()]

    temp = []
    for i in range(1,len(lists),3):
        temp.append(lists[i])

    stops = pd.DataFrame(np.array(temp))
    stops.columns = ['stop_id','stop_code','stop_name','stop_desc','LAT','LNG','zone_id','stop_url','location_type','parent_station']
    stops.drop('stop_code',axis = 1,inplace=True)
    stops.drop('stop_desc',axis = 1,inplace=True)
    stops.drop('zone_id',axis = 1,inplace=True)
    stops.drop('stop_url',axis = 1,inplace=True)
    stops.drop('location_type',axis = 1,inplace=True)
    stops.drop('parent_station',axis = 1,inplace=True)
    return stops

if __name__ == "__main__":
    stops_df = CLEAN_STOPSDATA()
    stops_df.to_csv('../../data/updated_data/substops_clean.csv', index=False)

