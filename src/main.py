# this is the main program file

import pandas as pd
from house_surroundings import get_univs_nearest_house

last_update_date = "10/11/2020"

# Read every cleaned database files
houses_file = "../data/updated_data/house_merged.csv"
houses_df = pd.read_csv(houses_file)

stops_file = "../data/updated_data/substops_clean.csv"
stops_df = pd.read_csv(stops_file)

theaters_file = "../data/updated_data/theater_clean.csv"
theaters_df = pd.read_csv(theaters_file)

restaurants_file = "../data/updated_data/restaurant_clean.csv"
restaurants_df = pd.read_csv(restaurants_file)

crime_file = "../data/updated_data/crime_clean.csv"
crime_df = pd.read_csv(crime_file)

covid19_file = "../data/updated_data/covid19_clean.csv"
covid19_df = pd.read_csv(covid19_file)

# longitude and latitude of different universities
location_list = [[-76.4786, 42.4485], [-73.9572, 40.8045], [-73.999499, 40.730537],
                 [-77.6283, 43.1283], [-73.6775, 42.7300], [-76.1340, 43.0377],
                 [-73.8840, 40.8565], [-73.9297, 40.8503], [-75.9699, 42.0893],
                 [-73.9898, 40.7345], [-74.9991, 44.6635], [-73.6003, 40.7088],
                 [-73.7912, 40.7010], [-74.0257, 40.7448], [-73.7956, 40.7219]]

universities = ["Cornell University", "Columbia University", "New York University",
                "University of Rochester", "Rensselaer Polytechnic Institute", "Syracuse University",
                "Fordham University", "Yeshiva University", "Binghamton University",
                "The New School", "Clarkson University", "Hofstra University",
                "City University of New York", "Stevens Institute of Technology", "St.John's University"]


def showDetailInfo(houseindex):
    house_info = houses_df.iloc[houseindex]
    print("house description: ", house_info.house_name)
    print("month price: ", house_info.price)
    print("street address: ", house_info.streetAddress)
    print("house type: ", house_info.house_type)
    print("postcode: ", house_info.postcode)

    print("""
Which of the following do you want to know more about this house?
1. Distance from nearest subway
2. 5 Nearby Restaurants
3. 3 Nearby Theaters
4. COVID19 data in past 4 weeks
5. Crime Report in past 5 years
Enter 0 for quiting the detailed search.
""")

    while True:
        try:
            ch = int(input("\nPlease enter the choice number:\nPress 0 for quit\n"))
            if ch == 1:
                print("The nearest subway is ", house_info.nearest_subway, " and is ",
                      house_info.distance_from_subway, " meters away.")
            elif ch == 2:
                # print 5 Nearby restaurants
                print("The most popular cuisine is: ", house_info.most_common_cuisine)
                print("Number restaurant within 500m: ", house_info.num_rests_within_500m)
                print("The 5 nearest restaurants are:\n")
                print("name\tcuisine\tstreet\tphone")

                restaurants_ls = house_info.nearest_5rests_index[1:-2].split(',')
                for i in restaurants_ls:
                    res = restaurants_df.iloc[int(i.strip())]
                    print(res['name'], "\t", res.cuisine, "\t", res.street, "\t", res.phone)

            elif ch == 3:
                # print 3 Nearby Theaters
                print("The 3 nearest theaters are:\n")
                print("name\ttel\turl\taddress\tzip")
                theater_ls = house_info.nearest_3theaters_index[1:-2].split(',')
                for i in theater_ls:
                    thetr = theaters_df.iloc[int(i.strip())]
                    print(thetr.THR_NAME, "\t", thetr.THR_TEL, "\t", thetr.THR_URL, "\t",
                          thetr.THR_ADDRESS, "\t", thetr.THR_ZIP)

            elif ch == 4:
                # print COVID19 data in past 4 weeks
                ZCTA = house_info.ZCTA
                covid_data = covid19_df[covid19_df['ZCTA'] == ZCTA].iloc[0]
                print("In the past four weeks, the COVID 19 data of here\n" + covid_data.NEIGHBORHOOD_NAME + "is: ")
                print("Total case count: ", covid_data.COVID_CASE_COUNT_4WEEK)
                print("Total case rate: ", covid_data.COVID_CASE_RATE_4WEEK)
                print("Total death count: ", covid_data.COVID_DEATH_COUNT_4WEEK)
                print("Total death rate: ", covid_data.COVID_DEATH_RATE_4WEEK)
                print("Number of people tested: ", covid_data.NUM_PEOP_TEST_4WEEK)
                print("Tested positive rate: ", covid_data.PERCENT_POSITIVE_4WEEK)
                print("Case counts change: ", covid_data.CASE_COUNT_CHANGE_4WEEK)

            elif ch == 5:
                # print Crime Report in past 5 years
                ZCTA = house_info.ZCTA
                try:
                    crime_data = crime_df[crime_df['ZCTA'] == ZCTA].iloc[0]
                    print("The house is in Precinct No.", crime_data.PCT_ID)
                    print("Crime rate of the precinct: ", crime_data.PCT_CRIME_RATE)
                    print("Borough of the precinct: ", crime_data.PCT_BORO_NAME)
                    print("Address of the precinct: ", crime_data.PCT_ADDR)
                except:
                    print("No crime record near this house so far")
            elif ch == 0:
                # quit the detailed searching
                break

            else:
                pass
        except():
            print("Invalid number.")


if __name__ == '__main__':

    # Start greetings:
    print("Hi, Welcome to CityMate's HouseRent Service!\n")
    print("Please specify your University, where do you want to live nearby?")

    count = 0
    for university in universities:
        count += 1
        print(str(count) + ". " + university)

    while True:
        try:
            uni = int(input("\nPlease enter the choice number of the university: "))
            if 1 <= uni <= 15:
                print("You would like to rent near " + universities[uni - 1])
                uni_chosen = uni
                break
            else:
                print("Invalid number.")
        except:
            pass

    print("\n......Now we are preparing data for you......\nWe have already updated data on " + last_update_date +
          """
Do you need to update local data (scraping again from sites)?
This may take a few hours.

If you want to update local data, press Y,
or press N for displaying rent information.
 """)

    while True:
        update_or_not = input("Please enter your input: ")
        if update_or_not == "Y" or update_or_not == "y":
            print("In this program, this will take too long, please press n")
            print("Update data manually by running update_data.py")
        elif update_or_not == "N" or update_or_not == "n":
            break
        else:
            pass

    print("\nLoading...... Please wait a few seconds!")
    all_nearest_houses_df = get_univs_nearest_house(houses_df, location_list)
    nearest_houses_index = all_nearest_houses_df.iloc[uni_chosen - 1].house_indexs[0:50]

    count = 0
    print("\nHere is information about 50 nearby houses for rent.")
    print("index\tname\tprice\tstreetAddress\tpostcode\thouse_type")
    for index in nearest_houses_index:
        count += 1
        info = houses_df.iloc[index]
        print(str(count) + "\t" + str(info.name) + "\t" + str(info.price) + "\t" + str(info.streetAddress) +
              "\t" + str(info.postcode) + "\t" + str(info.house_type))

    while True:
        try:
            ch = int(input("\nWhich house do you want to know more about?\n" +
                           "Please enter the index number for more information: "))
            if 1 <= ch <= 50:
                house_chosen = nearest_houses_index[ch - 1]
                showDetailInfo(house_chosen)  # row number index of house_df
            else:
                print("Invalid number.")
        except:
            pass

    print("Thank you for using our CityMate service, if you find our service useful, please recommend it to others!:)")
