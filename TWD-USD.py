# coding=utf-8
__author__ = 'john.chen'

import requests, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWD-USD"):
    os.mkdir("TWD-USD")
result =open("TWD-USD/TWD-USD.csv",'w') # 寫入模式：開頭用w，後來改為a，才能將資料都寫入清單

# 請在這裡修改日期，由於上限是"一年"，請改成XXXX/1/1 ~ XXXX/12/31
payload = {
    "download":"",
    "hdn_gostartdate":"2015/1/1",
    "hdn_goenddate":"2015/2/9",
    "syear":"2015",
    "smonth":"1",
    "sday":"1",
    "eyear":"2015",
    "emonth":"2",
    "eday":"9",
    "datestart":"2015/1/1",
    "dateend":"2015/2/9"
}
res = requests.post("http://www.taifex.com.tw/chinese/3/3_5.asp", data=payload)
#print res.encoding # 網頁編碼
soup = BeautifulSoup(res.text.encode("ISO-8859-1"))

counter = 0
for item in soup.select(".table_c tr"):
    counter += 1
    if counter == 1:
        t = item.text.split("\n")
        for item in t:
            result.write(item.encode('utf-8')  + " "),
            print item,
        counter = 0
        result.write(item.encode('utf-8') + "\n")
        print ""
print "清單產生完畢"
result.close()