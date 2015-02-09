# coding=utf-8
__author__ = 'john.chen'

import requests, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWD-USD"):
    os.mkdir("TWD-USD")
result =open("TWD-USD/TWD-USD.txt",'w') # 寫入模式：2006年用w，(含)2007後改為a，才能將資料都寫入清單

# 請在這裡修改日期，由於上限是"一年"，請改成XXXX/1/1 ~ XXXX/12/31
# 最早只到2006/5/29, 2008/6/23以前只有美金匯率
payload = {
    "download":"",
    "hdn_gostartdate":"2015/1/1",
    "hdn_goenddate":"2015/12/31",
    "syear":"2015",
    "smonth":"1",
    "sday":"1",
    "eyear":"2015",
    "emonth":"12",
    "eday":"31",
    "datestart":"2015/1/1",
    "dateend":"2015/12/31"
}
res = requests.post("http://www.taifex.com.tw/chinese/3/3_5.asp", data=payload)
#print res.encoding # 找出網頁編碼
soup = BeautifulSoup(res.text.encode("ISO-8859-1"))

counter = 0
for item in soup.select(".table_c tr")[1:]: # 除了2006以外，(含)2007年起必須加[1:]去掉表頭
    counter += 1
    if counter == 1:
        t = item.text.split("\n")
        for item in t:
            result.write(item.encode('utf-8') + " "),
            print item,
        counter = 0
        result.write(item.encode('utf-8') + "\n")
        print ""

# 提示結束跟關閉寫檔
print "清單產生完畢"
result.close()