import json
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


# agent data pasted from this blog:
# https://blog.csdn.net/qq_37597345/article/details/85319891
def get_random_agent():
    agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    agent = np.random.choice(agents)
    headers = {
        "User-Agent": agent,
        "Connection": 'close'
    }
    return headers


# download the html code, and return a string
def download_html(url):
    print("url is:", url)
    # s = re
    # r.keep_alive = False
    headers = get_random_agent()
    time.sleep(np.random.randint(0, 1))
    requests.adapters.DEFAULT_RETRIES = 10
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print("Access error ", r.status_code, ":", url)
            return ""
        html_str = str(r.text)
        r.close()
    except:
        print("Timeout error:", url)
        return ""
    return html_str


def get_urls(html_code):
    url_list = list()
    # soup = BeautifulSoup(html_code, 'html.parser')
    soup = BeautifulSoup(html_code, 'lxml')
    ul_list = soup.find_all("a", {"class": 'result-image gallery'})
    for ul in ul_list:
        href = ul.get('href')
        url_list.append(str(href))
    return url_list


def get_house_info(house_html):
    if house_html == "":
        return ["null", 0.0, 0.0, "$0", "null", "null", "null"]
    soup = BeautifulSoup(house_html, 'lxml')
    price = soup.find(class_="price")
    house_info_tags = soup.find_all("script", {"type": 'application/ld+json'})
    # print(house_info_tags[1].contents[0])
    house_info_string = str(house_info_tags[1])

    # get the json data in html
    start = 0
    count = 0
    end = 0
    for i in house_info_string:
        if i == '{':
            start = house_info_string.index(i)
            break
    for i in house_info_string:
        count += 1
        if i == "}":
            end = count
    house_json = json.loads(house_info_string[start:end])

    name = str(house_json['name'])
    longitude = float(house_json['longitude'])
    latitude = float(house_json['latitude'])
    price = price.string
    streetAddress = str(house_json['address']['streetAddress'])
    postcode = str(house_json['address']['postalCode'])
    house_type = str(house_json['@type'])
    house_info_list = [name, longitude, latitude, price, streetAddress, postcode, house_type]
    return house_info_list


def update_house_data():
    prefix = "https://newyork.craigslist.org/search/apa?housing_type=1&s="
    urls = list()
    for i in range(20):
        stuffing = 120 * i
        target_page = prefix + str(stuffing)
        html = download_html(target_page)
        urls += get_urls(html)

    # show all the urls to house page
    # print(urls)

    print(len(urls))

    with open("../../data/sites.txt", "w") as output_file:
        for i in urls:
            output_file.write(i)
            output_file.write("\n")
        output_file.close()

    # wait until writing the url data file is done.
    time.sleep(1)

    with open("../../data/sites.txt", "r") as input_file:
        original = input_file.readlines()
        urls = list()
        for i in original:
            # get rid of the '\n'
            urls.append(i[:-1])
        input_file.close()
    # print(urls)

    data = {
        'name': [],
        'longitude': [],
        'latitude': [],
        'price': [],
        'streetAddress': [],
        'postcode': [],
        'house_type': [],
    }
    df = pd.DataFrame(data)
    count_step = 0
    i = 0
    for url in urls:
        # save data checkpoints in case the program crashes.
        # if (i != 0) & (i % 100 == 0):
        #     file_name = "top " + str(i) + " houses.xlsx"
        #     df.to_excel(file_name, encoding='utf-8')
        count_step += 1
        print(count_step)
        house_html = download_html(url)
        df.loc[i] = get_house_info(house_html)
        i += 1

    # data cleaning, remove the empty lines
    new_df = pd.DataFrame(df)
    new_df = new_df.loc[new_df['name'] != "null"]
    return new_df

if __name__ == "__main__":
    update_house_data()
    new_df = update_house_data()
    new_df.to_csv("clean_house_data.csv", encoding='utf-8')