# author: Jingwen Ma, Yixuan Guo, Yue Jia, Yunxuan Yu, Zixin Yin
# Date: Oct-17, 2020

# This is the main program file, which imports numpy, pandas, PIL.Image, matplotlib.pyplot, wordcloud and house_surroundings
# It will fitst show you 15 universities and ask you to choose one of them. 
# After you enter the choice, 50 houses near the univesities will be shown.
# Chooce a single number(1-50) of the house you are interested in, 
# You will have a menu(enter 1-5 to choose, 0 to quit) of the house's surrounding information.

import numpy as np
import pandas as pd
import PIL.Image as image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
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
    
    # show the detail surrounding information menu
    print("""
Which of the following do you want to know more about this house?
1. Distance from nearest subway
2. 5 Nearby Restaurants
3. 3 Nearby Theaters
4. COVID19 data in past 4 weeks
5. Crime Report in past 5 years""")

    while True:
        try:
            ch = int(input("\nPlease enter the choice number(1-5):\nPress 0 for quit\n"))
            if ch == 1:
                print("\nThe nearest subway is ", house_info.nearest_subway, " and is ",
                      house_info.distance_from_subway, " meters away.")
            elif ch == 2:
                # print 5 Nearby restaurants
                print("\nThe most popular cuisine is: ", house_info.most_common_cuisine)
                print("Number restaurant within 500m: ", house_info.num_rests_within_500m)
                print("The 5 nearest restaurants are:\n")
                print("name\tcuisine\tstreet\tphone")

                restaurants_ls = house_info.nearest_5rests_index[1:-1].split(',')
                for i in restaurants_ls:
                    res = restaurants_df.iloc[int(i.strip())]
                    print(res['name'], "\t", res.cuisine, "\t", res.street, "\t", res.phone)

            elif ch == 3:
                # print 3 Nearby Theaters
                print("\nThe 3 nearest theaters are:\n")
                print("name\ttel\turl\taddress\tzip")
                theater_ls = house_info.nearest_3theaters_index[1:-1].split(',')
                for i in theater_ls:
                    thetr = theaters_df.iloc[int(i.strip())]
                    print(thetr.THR_NAME, "\t", thetr.THR_TEL, "\t", thetr.THR_URL, "\t",
                          thetr.THR_ADDRESS, "\t", thetr.THR_ZIP)

            elif ch == 4:
                # print COVID19 data in past 4 weeks
                ZCTA = house_info.ZCTA
                covid_data = covid19_df[covid19_df['ZCTA'] == ZCTA].iloc[0]
                print("\nIn the past four weeks, the COVID 19 data of here\n" + covid_data.NEIGHBORHOOD_NAME + "is: ")
                print("Total case count: ", covid_data.COVID_CASE_COUNT_4WEEK)
                print("Total case rate: ", covid_data.COVID_CASE_RATE_4WEEK)
                print("Total death count: ", covid_data.COVID_DEATH_COUNT_4WEEK)
                print("Total death rate: ", covid_data.COVID_DEATH_RATE_4WEEK)
                print("Number of people tested: ", covid_data.NUM_PEOP_TEST_4WEEK)
                print("Tested positive rate: ", covid_data.PERCENT_POSITIVE_4WEEK)
                print("Case counts change: ", covid_data.CASE_COUNT_CHANGE_4WEEK)

                # show line chart of covid19 cases in four weeks around the area.
                covid_case_list = [int(i.strip()) for i in covid_data.CASE_COUNT_CHANGE_4WEEK[1:-1].split(',')]
                x = np.array([1, 2, 3, 4])
                y = np.array(covid_case_list)
                plt.plot(x, y, color='red', linewidth=3.0)
                plt.xlabel('Week')
                plt.ylabel('Num of New Cases')
                plt.title('Covid-19 Cases In Four Weeks Around the House')
                plt.show()

            elif ch == 5:
                # print Crime Report in past 5 years
                ZCTA = house_info.ZCTA
                try:
                    crime_data = crime_df[crime_df['ZCTA'] == ZCTA].iloc[0]
                    print("\nThe house is in Precinct No.", crime_data.PCT_ID)
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


# show the word cloud of all restaurants' cuisines
def show_wordcloud(restaurant_df):
    # extract all types of restaurant speciaty into cuisine_list
    cuisine_raw = list()
    for rest_row in restaurant_df.iterrows():
        split_cuisines = (rest_row[1]['cuisine']).split(';')
        for sc in split_cuisines:
            cuisine_raw.append(sc)
    # transform all string into lower case
    cuisine_list = list()
    for i in cuisine_raw:
        cuisine_list.append(i.lower().strip())
    # count word frequency
    cuisine_dict = dict()
    for i in cuisine_list:
        if i in cuisine_dict:
            cuisine_dict[i] += 1
        else:
            cuisine_dict[i] = 1

    cuisine_dict = {k: v for k, v in sorted(cuisine_dict.items(), key=lambda item: item[1], reverse=True)}

    text = ""
    for i in cuisine_dict.keys():
        text += str(i) + ' '

    # America map is downloaded from google
    mask = np.array(image.open("../data/America.jpg"))
    wordcloud = WordCloud(mask=mask, background_color='white').generate_from_text(text)
    image_produce = wordcloud.to_image()
    image_produce.show()


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
            uni = int(input("\nPlease enter the choice number(1-15) of the university: "))
            if 1 <= uni <= 15:
                print("You would like to rent a house near " + universities[uni - 1])
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
    all_nearest_houses_df = get_univs_nearest_house(houses_df, location_list, uni_chosen)
    nearest_houses_index = all_nearest_houses_df.iloc[uni_chosen - 1].house_indexs[0:50]

    count = 0
    print("\nHere is information about 50 nearby houses for rent.")
    print("index\tname\tprice\tstreetAddress\tpostcode\thouse_type")
    for index in nearest_houses_index:
        count += 1
        info = houses_df.iloc[index]
        print(str(count) + "\t" + str(info.name) + "\t" + str(info.price) + "\t" + str(info.streetAddress) +
              "\t" + str(info.postcode) + "\t" + str(info.house_type))

    # Show the word cloud of all the restaurant in descending order.
    print("\nGenerating word cloud, please wait...")
    show_wordcloud(restaurants_df)

    while True:
        try:
            ch = int(input("\nWhich house do you want to know more about?\n" +
                           "Please enter the index number(1-50) for more information:\n"
                           "Enter 0 to exit\n"))
            if 1 <= ch <= 50:
                house_chosen = nearest_houses_index[ch - 1]
                showDetailInfo(house_chosen)  # row number index of house_df
            elif ch == 0:
                break
            else:
                print("Invalid number.")
        except:
            pass

    print("Thank you for using our CityMate service, if you find our service useful, please recommend it to others!:)")
