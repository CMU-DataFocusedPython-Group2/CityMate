import sys, os
sys.path.append(os.getcwd()[:-13])
from clean_crime import GET_CRIME_RAW, CLEAN_CRIMEDATA
from clean_stops import GET_STOPS_RAW, CLEAN_STOPSDATA
from clean_theater import GET_THEATER_DF
from clean_restaurant import GET_RESTAURANT_DF
from clean_covid19 import GET_COVID19_DF
from clean_house import update_house_data
from house_surroundings import *


def UPDATE_DATA():
    # update crime data
    print("Updating crime data...")
    GET_CRIME_RAW()
    CRIME_DF = CLEAN_CRIMEDATA()
    CRIME_DF.to_csv('../../data/updated_data/crime_clean.csv', index=False)
    print("Crime data updated.")

    # update subway stops data
    print("")
    print("Updating subway stops data...")
    GET_STOPS_RAW()
    SUBSTOPS_DF = CLEAN_STOPSDATA()
    SUBSTOPS_DF.to_csv('../../data/updated_data/substops_clean.csv', index=False)
    print("Subway stops data updated.")

    # update restaurant data
    print("")
    print("Updating restaurants data...")
    RESTAURANT_DF = GET_RESTAURANT_DF()
    RESTAURANT_DF.to_csv('../../data/updated_data/restaurant_clean.csv', index=False)
    print("Restaurants data updated.")

    # update theater data
    print("")
    print("Updating theaters data...")
    THEATER_DF = GET_THEATER_DF()
    THEATER_DF.to_csv('../../data/updated_data/theater_clean.csv', index=False)
    print("Theaters data updated.")

    # update covid19 data
    print("")
    print("Updating COVID19 data...")
    COVID19_DF = GET_COVID19_DF()
    COVID19_DF.to_csv('../../data/updated_data/covid19_clean.csv', index=False)
    print("COVID19 data updated.")


def UPDATE_HOUSE_DATA():
    # updata house data
    print("")
    print("Updating house data... This may take half a day")
    HOUSE_DF = update_house_data()
    HOUSE_DF.to_csv('../../data/updated_data/house_clean.csv', index=False)
    print("House data updated.")
    return


def GET_HOUSE_DF():
    # merge house data
    print("")
    print("Merging house data... This may take 6 or 7 minutes")
    stops_file = "../../data/updated_data/substops_clean.csv"
    stops_df = pd.read_csv(stops_file)

    restaurants_file = "../../data/updated_data/restaurant_clean.csv"
    rest_df = pd.read_csv(restaurants_file)

    theaters_file = "../../data/updated_data/theater_clean.csv"
    cinema_df = pd.read_csv(theaters_file)

    houses_df = get_house_df_1()
    houses_df = get_nearest_3cinemas(houses_df, cinema_df)
    houses_df = get_surrounding_restaurants(houses_df, rest_df)
    houses_df = get_subway_distance(houses_df, stops_df)

    houses_df.to_csv('../../data/updated_data/house_merged.csv', index=False)
    print("Merging completed.")
    print("All update process completed.")
    return


if __name__ == "__main__":
    UPDATE_DATA()
    GET_HOUSE_DF()
