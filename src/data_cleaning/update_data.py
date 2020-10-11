from clean_crime import GET_CRIME_RAW, CLEAN_CRIMEDATA
from clean_stops import GET_STOPS_RAW, CLEAN_STOPSDATA
from clean_theater import GET_THEATER_DF
from clean_restaurant import GET_RESTAURANT_DF
from clean_covid19 import GET_COVID19_DF
from clean_house import update_house_data

def UPDATE_DATA():
    GET_CRIME_RAW()
    CRIME_DF = CLEAN_CRIMEDATA()
    CRIME_DF.to_excel('updated_data/crime_clean.xls', sheet_name='data', index=False)
    GET_STOPS_RAW()
    SUBSTOPS_DF = CLEAN_STOPSDATA()
    SUBSTOPS_DF.to_excel('updated_data/substops_clean.xls', sheet_name='data', index=False)
    RESTAURANT_DF = GET_RESTAURANT_DF()
    RESTAURANT_DF.to_excel('updated_data/restaurant_clean.xls', sheet_name='data', index=False)
    THEATER_DF = GET_THEATER_DF()
    THEATER_DF.to_excel('updated_data/theater_clean.xls', sheet_name='data', index=False)
    COVID19_DF = GET_COVID19_DF()
    COVID19_DF.to_excel('updated_data/covid19_clean.xls', sheet_name='data', index=False)
    return

def UPDATE_HOUSE_DATA():
    HOUSE_DF = update_house_data()
    HOUSE_DF.to_excel('updated_data/house_clean.xls', sheet_name='data', index=False)
    return

if __name__ == "__main__":
    UPDATE_DATA()