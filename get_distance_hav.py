#!/usr/bin/env python
# coding: utf-8

# In[1]:


from math import sin, asin, cos, radians, fabs, sqrt
 
EARTH_RADIUS=6371           # earth's average radius is 6371km
 
def hav(theta):
    s = sin(theta / 2)
    return s * s
 
def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # The distance between two points on the sphere is calculated by haverne formula.
    # Conversion the longitude and latitude to radian
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
 
    return distance
 
lon1,lat1 = (22.599578, 113.973129) #深圳野生动物园(起点）
lon2,lat2 = (22.6986848, 114.3311032) #深圳坪山站 (百度地图测距：38.3km)
d2 = get_distance_hav(lon1,lat1,lon2,lat2)
print(d2)

