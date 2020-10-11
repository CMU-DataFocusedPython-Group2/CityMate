# this is the main program file

import pandas as pd

last_update_date = "10/11/2020"

# Read every cleaned database files
houses_file = "./data/clean_house_data.xlsx"
houses_df = pd.read_excel(houses_file)

stops_file = "./data/clean_stops_data.csv"
stops_df = pd.read_csv(stops_file)

# theaters_file = "./data/clean_theater.xlsx"
# theaters_df = pd.read_excel(theaters_file)

restaurants_file = "./data/restaurant_point.csv"
restaurants_df = pd.read_csv(restaurants_file)

# crime_file = "./data/clean_crime_data.xlsx"
# crime_df = pd.read_excel(crime_file)

def showDetailInfo(houseindex):
    print("""
Which of the following do you want to know more about this house?
1. 3 Nearby Subway Stops
2. 10 Nearby Restaurants
3. 10 Nearby Theaters
4. COVID19 data in past 4 weeks
5. Crime Report in past x years
Enter 0 for quiting the detailed search.
""")

    while(True):
        try:
            ch = int(input("Please enter the index number: "))
            if ch == 1:
                pass
            elif ch == 2:
                pass
            elif ch == 3:
                pass
            elif ch == 4:
                pass
            elif ch == 5:
                pass
            elif ch == 0:
                pass # quit the detailed seraching
                break
            else:
                pass
        except:
            pass


if __name__ == '__main__':
    # Start greetings:
    print("Hi, Welcome to CityMate's HouseRent Service!\n")
    print("Please specify your University, where do you want to live nearby?")

    universities = ["Cornell University", "Columbia University", "New York University",
                    "University of Rochester","Rensselaer Polytechnic Institute","Syracuse University",
                    "Fordham University","Yeshiva University","Binghamton University",
                    "The New School","Clarkson University","Hofstra University",
                    "City University of New York", "Stevens Institute of Technology","St.John's University"]
    count = 0
    for university in universities:
        count += 1
        print(str(count) + ". " + university)

    while(True):
        try:
            uni = int(input("\nPlease enter the index number of the university: "))
            if 1<=uni<=15:
                print("You would like to rent near " + universities[uni-1])
                break
        except:
            pass


    # location_list = [[-76.4786,42.4485], [-73.9572,40.8045], [-73.999499,40.730537],
    #                  [-77.6283,43.1283], [-73.6775,42.7300], [-76.1340,43.0377],
    #                  [-73.8840,40.8565], [-73.9297,40.8503], [-75.9699,42.0893],
    #                  [-73.9898,40.7345], [-74.9991,44.6635], [-73.6003, 40.7088],
    #                  [-73.7912,40.7010], [-74.0257,40.7448], [-73.7956,40.7219]]

    print("\n......Now we are preparing data for you......\nWe have already updated data on " + last_update_date +
          """
Do you need to update local data (scraping again from sites)?
This may take a few hours.

If you want to update local data, press Y, 
or press N for displaying rent information.
 """)

    while(True):
        update_or_not = input("Please enter your input: ")
        if update_or_not=="Y" or update_or_not =="y":
            # call the update function
            pass
        elif update_or_not == "N" or update_or_not == "n":
            break
        else:
            pass

    print("\nHere is information about 50 nearby houses for rent.")

    while(True):
        try:
            ch = int(input("\nWhich house do you want to know more about?\n" +
                           "Please enter the index number for more information: "))
            if 1<=ch<=50:
                showDetailInfo(ch)
            else:
                continue
        except:
            pass

    print("Thank you for using our CityMate service, if you find our service useful, please recommend it to others!:)")