#!/usr/bin/env python
# coding: utf-8

# In[24]:


# house surrounding information, include 6 functions:
# hav(),get_distance_hav(),get_house_df(),get_univs_nearest_house(),get_nearest_3cinemas(),get_surrounding_restaurants
import pandas as pd
import numpy as np
import random
from math import sin, asin, cos, radians, fabs, sqrt
from collections import Counter
 
def hav(theta):
    s = sin(theta / 2)
    return s * s
 
def get_distance_hav(lat0, lng0, lat1, lng1):
    
    # The distance between two points on the sphere is calculated by haverne formula.

    # Conversion the longitude and latitude to radian
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    earth_radius=6371   # earth's average radius is 6371km
    distance = 2 * earth_radius * asin(sqrt(h))
 
    return distance

def get_house_df_1():
    house = pd.read_excel('../data/clean_house_data.xlsx')
    house.columns = ['house_id', 'house_name', 'LNG', 'LAT', 'price', 'streetAddress', 'postcode', 'house_type']
    house.drop('house_id', axis=1, inplace=True)
    # return a house dataframe
    return house

def get_univs_nearest_house(house,univs_location):   #参数需调整,univ是list还是df希望整合的同学视情况而定
    univs_house_dis = []
    for univ in univs_location:
        univ_house_dis = []
        for house_row in house.iterrows():
            dis = get_distance_hav(float(house_row[1][1]),float(house_row[1][2]),float(univ[0]),float(univ[1]))+ 0.001 * random.random()
            univ_house_dis.append(dis)
        d = dict(zip(univ_house_dis,range(len(univ_house_dis))))
        univ_house_dis.sort()
        a = []
        for uhd in univ_house_dis:
            if len(a) <= 50:
                a.append(d.get(uhd))
        univs_house_dis.append(a) 
    
    univs = pd.DataFrame(np.array(univs_location),columns = ['LNG','LAT'])
    univs['house_indexs'] = univs_house_dis
    
    return univs  # return a univs dataframe

def get_nearest_3cinemas(house,cinema_df):# 最好是能传一个有index的cinema进来,我这里index是第8列 => index[7]
    # calculate the nearest 3 cinemas for each house
    nearest3cinemas = []
    
    cinema = pd.read_csv("../data/updated_data/cinema_clean.csv",header=0)        #参数修正后可删
    cinema['index'] = [i for i in range(len(cinema))]                             #参数修正后可删
    
    for house_row in house.iterrows():        
        nearest_index = [0,0,0]  # initialize a nearest_index to store the nearest 3 cinemas' index
        first_nearest = 999999   # initialize the distance from each house to the nearest cinema
        second_nearest = 999999  # initialize the distance from each house to the second nearest cinema
        third_nearest = 999999   # initialize the distance from each house to the third nearest cinema
        
        for cinema_row in cinema.iterrows():
            dis = get_distance_hav(float(house_row[1][1]),float(house_row[1][2]),float(cinema_row[1][0]),float(cinema_row[1][1]))
            # search nearest 3 cinema by brute force
            if dis < first_nearest: 
                third_nearest = second_nearest
                second_nearest = first_nearest
                first_nearest = dis
                nearest_index[2] = nearest_index[1]
                nearest_index[1] = nearest_index[0] 
                nearest_index[0] = cinema_row[1][7]   #index column num
            if dis > first_nearest and dis < second_nearest: 
                third_nearest = second_nearest
                second_nearest = dis
                nearest_index[2] = nearest_index[1]
                nearest_index[1] = cinema_row[1][7]   #index column num
            if dis > second_nearest and dis < third_nearest: 
                third_nearest = dis
                nearest_index[2] = cinema_row[1][7]   #index column num
        nearest3cinemas.append(nearest_index)
        
    house['nearest_3cinemas_index'] = nearest3cinemas # insert the nearest3cinemas column

    return house    # return input house's dataframe after inserting a 'nearest_3cinemas_index column'


def get_surrounding_restaurants(house,rest_df):#参数要求同get_nearest_3cinemas
    
    # calculate the nearest 5 restaurants,restaurants number within 500m and the most common cuisine within 500m for each house
    
    rest = pd.read_csv("../data/updated_data/restaurant_clean.csv",header=0)  #参数修正后可删
    rest['index'] = [i for i in range(len(rest))]        #参数修正后可删

    common_cuisines = []          # store common cuisines for each house
    num_rests_within_500m = []
    nearest5rests = []
    
    for house_row in house.iterrows():
        cuisines = []# store each row's cuisines
        nearest_index = [0,0,0,0,0]
        first_nearest = 999999
        second_nearest = 999999
        third_nearest = 999999
        fourth_nearest = 999999
        fifth_nearest = 999999
        for rest_row in rest.iterrows():
            dis = get_distance_hav(float(house_row[1][1]),float(house_row[1][2]),float(rest_row[1][0]),float(rest_row[1][1]))*1000 
            if dis <= 500:
                split_cuisines = (rest_row[1][3]).split(';')
                for sc in split_cuisines:
                    cuisines.append(sc)

            # calculate the nearest 5 restaurants  
            if dis < first_nearest: 
                fifth_nearest = fourth_nearest
                fourth_nearest = third_nearest
                third_nearest = second_nearest
                second_nearest = first_nearest
                first_nearest = dis
                nearest_index[4] = nearest_index[3]
                nearest_index[3] = nearest_index[2]
                nearest_index[2] = nearest_index[1]
                nearest_index[1] = nearest_index[0]
                nearest_index[0] = rest_row[1][6]#index column num
            if dis > first_nearest and dis < second_nearest:             
                fifth_nearest = fourth_nearest
                fourth_nearest = third_nearest
                third_nearest = second_nearest
                second_nearest = dis
                nearest_index[4] = nearest_index[3]
                nearest_index[3] = nearest_index[2]
                nearest_index[2] = nearest_index[1]
                nearest_index[1] = rest_row[1][6]#index column num
            if dis > second_nearest and dis < third_nearest: 
                fifth_nearest = fourth_nearest
                fourth_nearest = third_nearest
                third_nearest = dis
                nearest_index[4] = nearest_index[3]
                nearest_index[3] = nearest_index[2]
                nearest_index[2] = rest_row[1][6]#index column num
            if dis > second_nearest and dis < third_nearest: 
                fifth_nearest = fourth_nearest
                fourth_nearest = dis
                nearest_index[4] = nearest_index[3]
                nearest_index[3] = rest_row[1][6]#index column num
            if dis > second_nearest and dis < third_nearest: 
                fifth_nearest = dis
                nearest_index[4] = rest_row[1][6]#index column num
            
        common_cuisines.append(Counter(cuisines).most_common(1))
        num_rests_within_500m.append(len(cuisines))
        nearest5rests.append(nearest_index)
        
    # get the most common cuisine for each house
    most_common_cuisine = []
    for i in common_cuisines:
        if (len(i) == 0): most_common_cuisine.append("")
        else: most_common_cuisine.append(i[0][0])
            
    #add three columns to house
    house['most_common_cuisine'] = most_common_cuisine
    house['num_rests_within_500m'] = num_rests_within_500m
    house['nearest_5rests_index'] = nearest5rests
    
    return house


def get_subway_distance(house,stopsdf):
    
    stops = pd.read_csv("../data/updated_data/stops_clean.csv",header=0)
    min_distance = []
    subway_names = []
    for house_row in house.iterrows():
        imin = 999999
        subway_name = ""
        for stops_row in stops.iterrows():
            hts_dis = get_distance_hav(float(house_row[1][1]),float(house_row[1][2]),float(stops_row[1][3]),float(stops_row[1][2]))
            if hts_dis < imin:
                imin = hts_dis
                subway_name = stops_row[1][1]
        min_distance.append(imin)
        subway_names.append(subway_name)

    house['distance_from_subway'] = min_distance
    house['distance_from_subway'] *= 1000
    house['nearest_subway'] = subway_names
    
    return house

