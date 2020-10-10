import requests
import json
import pandas as pd
import xlwt
from sodapy import Socrata
from shapely.geometry import Point, Polygon
from bs4 import BeautifulSoup

# crime data details from API and write it to a file
'''req1 = requests.get('https://data.cityofnewyork.us/resource/qgea-i56i.json')
f1 = open('crime_details.txt','wt')
f1.write(req1.text)
f1.close()'''

client = Socrata("data.cityofnewyork.us", 'weom0t1xmEmSCKQihBJ7FJ4kT')
results = client.get("pri4-ifjk", limit=2000)
results_df = pd.DataFrame.from_records(results)
modzcta_df = results_df.drop(['label','zcta','pop_est'],axis=1).set_index('modzcta',drop=True)

# function that convert longitute-latitude to ZCTP code
def LngLat_to_ZCTP(Lng,Lat):
    p1 = Point(Lng,Lat)
    i = 0
    while(i<=len(modzcta_df.index)-1):
        poly = Polygon(modzcta_df.iloc[i].the_geom['coordinates'][0][0])
        if(p1.within(poly)):
            return modzcta_df.iloc[i].name
        else:
            i += 1
    i = 0
    while(i<=len(modzcta_df.index)-1):
        poly = Polygon(modzcta_df.iloc[i].the_geom['coordinates'][0][0])
        dis = poly.centroid.distance(p1)
        if i==0:
            min_dis = dis
            name = modzcta_df.iloc[i].name
        elif dis < min_dis:
            min_dis = dis
            name = modzcta_df.iloc[i].name
        i += 1
    return(name)

# crime_count count the num of crime reports for each pct and sort it
crime_count = {}
f2 = open('crime_details.txt','rt')
crime_details = f2.readlines()[:-1]
for rec in crime_details:
    t_rec = json.loads(rec[1:-1])
    crime_count[t_rec['addr_pct_cd']] = crime_count.get(t_rec['addr_pct_cd'],0)+1
crime_count = sorted(crime_count.items(), key=lambda d: int(d[0]), reverse=False)

# use beautiful soup web scraping to find the addr of each police precinct
req2 = requests.get('https://www1.nyc.gov/site/nypd/bureaus/patrol/precincts-landing.page')
req2_bs = BeautifulSoup(req2.text, "lxml")
target_addr = req2_bs.findAll('td', {"data-label" : "Address"})
precinct_addr = []
for row in target_addr:
    precinct_addr.append(row.contents[0])
# find the ID of each police precinct and match it with its addr
target_police_prc = req2_bs.findAll('td', {"data-label" : "Precinct"})
precinct_seq = []
new_seq = []
for row in target_police_prc:
    precinct_seq.append(row.find('a').contents[0].split(' ')[0])
# convert the 3nd, 14th etc. to integer numbers
for item in precinct_seq:
    if item[-2:] == 'st' or  item[-2:] == 'nd' or item[-2:] == 'st' or item[-2:] == 'th' or \
    item[-2:] == 'rd':
        new_seq.append(item[0:-2])
    else:
        new_seq.append(item)

# calculate the ZCTP for each police precincts, and organize them in a dict pct_ZCTP
pct_ZCTP = {}
for rec in crime_details:
    t_rec = eval(rec[1:-1])
    pct_ZCTP[t_rec['addr_pct_cd']] = LngLat_to_ZCTP(float(t_rec.get('longitude', 0)), float(t_rec.get('latitude', 0)))

# convert crime_count to a list of lists, key!!!
crime_count_list = []
for row in crime_count:
    crime_count_list.append(list(row))
for row in crime_count_list:
    # calculate the crime rate for each police precincts
    row[1] /= len(crime_details)/100
    row[1] = str(round(row[1],2)) + '%'
    # construct each row
    for rec in crime_details:
        # append the borough names
        t_rec = json.loads(rec[1:-1])
        if(t_rec['addr_pct_cd'] == row[0]):
            row.append(t_rec.get('boro_nm','None'))
            break
    is_AddAddr = False
    for i in range(len(new_seq)):
        # append the addresses
        if(new_seq[i] == row[0]):
            row.append(precinct_addr[i])
            is_AddAddr = True
            break
    # append the ZCTPs
    if is_AddAddr:
        row.append(pct_ZCTP[row[0]])
    else:
        row.append('None')
        row.append(pct_ZCTP[row[0]])

# write to excel
crime_count_df = pd.DataFrame(crime_count_list, columns = ['PCT_ID', 'PCT_CRIME_RATE', 'PCT_BORO_NAME', 'PCT_ADDR', 'ZCTP'])
crime_count_df.to_excel('crime_clean.xls', sheet_name='data', index=False)
