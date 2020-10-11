import requests
import pandas as pd

def GET_THEATER_DF():
    dl_addr = 'https://data.cityofnewyork.us/api/views/2hzz-95k8/rows.csv?accessType=DOWNLOAD'
    req = requests.get(dl_addr)
    theater_csv = req.text.split('\n')

    # read the csv raw data, and append the information of each theater in NYC into a list of lists
    #cinema_csv = open('cinema_raw.csv')
    list_of_lists = []
    for line in theater_csv[:-1]:
        row = line.split(',')
        if(row[6] == "New York"):
            list_of_lists.append(row)

    # revise the list of lists to just get what we want
    new_list = []
    for lt in list_of_lists[1:]:
        lt = lt[0][7:-1].split() + lt[1:5] + lt[7:]
        new_list.append(lt)

    # convert the list of lists to a dataframe and write it to excel
    col = ['LNG','LAT','THR_NAME','THR_TEL' ,'THR_URL','THR_ADDRESS',"THR_ZIP"]
    theater_df = pd.DataFrame(new_list, columns = col)
    theater_df.index = range(1, len(theater_df) + 1)
    return theater_df

if __name__ == "__main__":
    theater_df = GET_THEATER_DF()
    theater_df.to_csv('../../data/updated_data/theater_clean.csv', index=False)
