from clean_crime import GET_CRIME_RAW, CLEAN_CRIMEDATA
from clean_stops import GET_STOPS_RAW, CLEAN_STOPSDATA
from clean_theater import GET_THEATER_DF
from clean_restaurant import GET_RESTAURANT_DF
from clean_covid19 import GET_COVID19_DF
from clean_house import update_house_data

def UPDATE_DATA():
    # update crime data
    print("Collecting crime data...")
    GET_CRIME_RAW()
    CRIME_DF = CLEAN_CRIMEDATA()
    CRIME_DF.to_csv('../../data/updated_data/crime_clean.csv', index=False)

    '''# update subway stops data
    print("Collecting subway stops data...")
    GET_STOPS_RAW()
    SUBSTOPS_DF = CLEAN_STOPSDATA()
    SUBSTOPS_DF.to_csv('../../data/updated_data/substops_clean.csv', index=False)

    # update restaurant data
    print("Collecting restaurants data...")
    RESTAURANT_DF = GET_RESTAURANT_DF()
    RESTAURANT_DF.to_csv('../../data/updated_data/restaurant_clean.csv', index=False)

    #update theater data
    print("Collecting theaters data...")
    THEATER_DF = GET_THEATER_DF()
    THEATER_DF.to_csv('../../data/updated_data/theater_clean.csv', index=False)

    # update covid19 data
    print("Collecting COVID19 data...")
    COVID19_DF = GET_COVID19_DF()
    COVID19_DF.to_csv('../../data/updated_data/covid19_clean.csv', index=False)'''

def UPDATE_HOUSE_DATA():
    # updata house data
    HOUSE_DF = update_house_data()
    HOUSE_DF.to_csv('../../data/updated_data/house_clean.csv', index=False)

if __name__ == "__main__":
    UPDATE_DATA()