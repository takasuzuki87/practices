
# coding: utf-8

# In[164]:
import time
import pandas as pd
import numpy as np


# In[3]:
import requests
import bs4
import urllib


# In[58]:
#quit()


# ## 食べログから東京23区のピザレストランの情報取得を試みる
#
# まずは千代田区で個々に試し
# In[132]:
# URL of the page showing pizza restaurants in Chiyoda
url_pz = "https://tabelog.com/tokyo/C13101/rstLst/pizza/1/"

# Download url_pz
resp_pz = requests.get(url_pz)
# Retreive headers
#print(resp_pz.headers)


# In[133]:
# HTMLの内容を取得するには".text"とする。
html_pz = resp_pz.text
soup_pz = bs4.BeautifulSoup(html_pz, "lxml")


# In[134]:
# Pickup address
addresses = soup_pz.find_all('p', class_="list-rst__address cpy-address")

# Obtain all addresses on the first page
list_1 = []
for address in addresses:
    a = address.text
    list_1.append(a)
print(list_1)
print(len(list_1))


# In[135]:
# Pickup restaurant name
name = soup_pz.find_all('a', class_="list-rst__rst-name-target cpy-rst-name")

# Obtain all names on the first page
name_list = []
for nm in name:
    n = nm.text
    name_list.append(n)
print(name_list)
print(len(name_list))


# In[43]:
# Pickup score
score = soup_pz.find_all('span', class_="c-rating__val c-rating__val--strong list-rst__rating-val")

# Obtain all scores on the first page
score_list = []
for sc in score:
    s = sc.text
    score_list.append(s)
print(score_list)
print(len(score_list))


# In[44]:
# Pickup reviews
reviews = soup_pz.find_all('em', class_="list-rst__rvw-count-num cpy-review-count")

# Obtain all scores on the first page
rev_list = []
for re in reviews:
    r = re.text
    rev_list.append(r)
print(rev_list)
print(len(rev_list))


# In[47]:
# Pickup dinner budget
budget = soup_pz.find_all('span', class_="c-rating__val list-rst__budget-val cpy-dinner-budget-val")

# Obtain all scores on the first page
budget_list = []
for bud in budget:
    b = bud.text
    budget_list.append(b)
print(budget_list)
print(len(budget_list))


# Get information from each restaurant

# In[99]:
ultag = soup_pz.find_all('ul', class_= "js-rstlist-info rstlist-info")
#print(ultag[0])


# In[100]:
# https://stackoverflow.com/questions/17246963/how-to-find-all-lis-within-a-specific-ul-class
rest_li1 = ultag[0].find_all('li', class_="list-rst js-bookmark js-rst-cassette-wrap js-is-need-redirect")
rest_li2 = ultag[0].find_all('li', class_="list-rst js-bookmark js-rst-cassette-wrap")
rest_li = rest_li1 + rest_li2
#print(rest_li)


# In[101]:
#get information of each restaurant

df = []
for li in rest_li:
    address = li.find('p', class_="list-rst__address cpy-address").text
    name = li.find('a', class_="list-rst__rst-name-target cpy-rst-name").text
    s = li.find('span', class_="c-rating__val c-rating__val--strong list-rst__rating-val")
    if s is not None:
        score = s.text
    else:
        score = "-"
    review = li.find('em', class_="list-rst__rvw-count-num cpy-review-count").text
    budget = li.find('span', class_="c-rating__val list-rst__budget-val cpy-dinner-budget-val").text

    restinfo = [name, address,score,review, budget]
    #df_rest0 = pd.DataFrame(restinfo).T
    #df_rest = df_rest.append(df_rest0)
    df.append(restinfo)
#print(df)


# In[102]:
df1 = pd.DataFrame(data=df)
#df1


# ## Try the script on multiple pages

# In[314]:
# Change the last two digits of the area portion (C131**) in the base_url_pz below
base_url_pz = "https://tabelog.com/tokyo/C13123/rstLst/pizza/"

def scrape_address_pz(url_pz):
    resp_pz = requests.get(url_pz)
    html_pz = resp_pz.text
    soup_pz = bs4.BeautifulSoup(html_pz, "lxml")
    ultag = soup_pz.find_all('ul', class_= "js-rstlist-info rstlist-info")
    rest_li1 = ultag[0].find_all('li', class_="list-rst js-bookmark js-rst-cassette-wrap js-is-need-redirect")
    rest_li2 = ultag[0].find_all('li', class_="list-rst js-bookmark js-rst-cassette-wrap")
    rest_li = rest_li1 + rest_li2

    df_pz0 = []
    for li in rest_li:
        address = li.find('p', class_="list-rst__address cpy-address").text
        name = li.find('a', class_="list-rst__rst-name-target cpy-rst-name").text
        s = li.find('span', class_="c-rating__val c-rating__val--strong list-rst__rating-val")
        if s is not None:
            score = s.text
        else:
            score = "-"
        review = li.find('em', class_="list-rst__rvw-count-num cpy-review-count").text
        budget = li.find('span', class_="c-rating__val list-rst__budget-val cpy-dinner-budget-val").text

        restinfo = [name,address,score,review,budget]
        df_pz0.append(restinfo)

    return(df_pz0)

def scrape_main_pz(page_pz):
    url_pz = base_url_pz+ "%d/" %page_pz
    df_pz1 = scrape_address_pz(url_pz)
    #time.sleep(3)
    return(df_pz1)


# In[315]:
soup_pz_1 = bs4.BeautifulSoup(requests.get(base_url_pz).text, "lxml")
#print(int(soup_pz_1.find_all('span', class_="list-condition__count")[0].text)//20 + 1)


# In[316]:
df_pz2 = []
max_attempts = 10
total_pages = int(soup_pz_1.find_all('span', class_="list-condition__count")[0].text)//20 + 1
page_numbers = range(1,int(total_pages)+1)

for page_pz in page_numbers:
    for attempt in range(max_attempts):
        try:
            df_pz1 = scrape_main_pz(page_pz)
            df_pz2.extend(df_pz1)
            print("ページ",page_pz,"をスクレイプしました")
        except requests.exceptions.Timeout:
            print("接続タイムアウト。2分後に再試行します...")
            time.sleep(120)
            continue # 最も内側の forに戻る
        except requests.exceptions.RequestException as e:
            print("%s. 5分後に再試行します..." % e.message)
            time.sleep(300)
            continue # 最も内側の forに戻る
        #　エラー無しの場合attempループを脱出して、次のページのループに戻る
        break


# In[317]:
df_pz = pd.DataFrame(data = df_pz2)
print(len(df_pz))
#df_pz


# Name columns, reformat address

# In[318]:
# Reformat df_pz and export as .csv

df_pz.columns = ['Name', 'Address', 'Score', 'Reviews', 'Budget']
#df_pz.head(2)

Address = df_pz['Address']

address_list = []
for row in Address:
    space = row.find(' ')
    if space < 0:
        main_address = row
    else:
        main_address = row[:space]
    address_list.append(main_address)
#print(address_list)

df_pz['Address'] = address_list

df_pz.head(2)


# In[319]:
df_pz.to_csv("Edogawa_pz.csv", index=False, encoding="utf-8")


# Cancatinate all csv files

# In[334]:
import os
filenames = [f for f in os.listdir() if f.endswith('_pz.csv')]

print(filenames)


# In[336]:
pieces = []
for filename in filenames:
    frame = pd.read_csv(filename)
    pieces.append(frame)


# In[338]:
dfpz = pd.concat(pieces, ignore_index=True)


# In[340]:
dfpz.head()

dfpz.to_csv("Tokyo_pz.csv", index=False, encoding="utf-8")
