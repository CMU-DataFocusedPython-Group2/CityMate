#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

path = 'stops.txt'
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
stops


outputpath='clean_stops_data.csv'
stops.to_csv(outputpath,sep=',',index=False,header=True)
