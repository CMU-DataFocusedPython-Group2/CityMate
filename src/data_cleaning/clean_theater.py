import requests
import pandas as pd

#dl_addr = 'https://data.cityofnewyork.us/api/views/2hzz-95k8/rows.csv?accessType=DOWNLOAD'
#cinema_csv = requests.get(dl_addr)

# read the csv raw data, and append the information of each theater in NYC into a list of lists
cinema_csv = open('cinema_raw.csv')
list_of_lists = []
for line in cinema_csv:
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
cinema_df = pd.DataFrame(new_list, columns = col)
cinema_df.index = range(1,len(cinema_df) + 1)
cinema_df.to_excel('cinema_clean.xls',sheet_name='data', index=False)
