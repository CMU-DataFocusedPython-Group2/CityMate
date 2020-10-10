# group_2_CityMate_project.py
# this is the main program file

import pandas as pd

# Read every cleaned database files
houses_file = "../data/clean_house_data.xlsx"
houses_df = pd.read_excel(houses_file)

stops_file = "../data/clean_stops_data.csv"
stops_df = pd.read_csv(stops_file)

theaters_file = "../data/clean_theater.xlsx"
theaters_df = pd.read_excel(theaters_file)

restaurants_file = "../data/restaurant_point.csv"
restaurants_df = pd.read_csv(restaurants_file)

crime_file = "../data/clean_crime_data.xlsx"
crime_df = pd.read_excel(crime_file)



if __name__ == '__main__':
    # Start greetings:
    print("Hi, this is CityMate Service.")

    print("do you need to update local data(scraping again from sites)?\n this may take a few hours.")

    # loop
    while ():
        print("Please input the name of your university:")
        # add position here

        print("Do you want to know:\n")
        print("1.house renting\n"
              "2.nearby movie theaters\n"
              "3.restaurants"
              "4.crime in this area")

        ch = input()

        # if ch == '1':
            # add more search here
        # ...