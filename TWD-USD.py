# coding=utf-8
__author__ = 'john.chen'

import requests, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWD-USD"):
    os.mkdir("TWD-USD")

# 總共34頁
for page in range(1,35):
    res = requests.get("http://www.cbc.gov.tw/lp.asp?CtNode=645&CtUnit=308&BaseDSD=32&mp=1&nowPage=%d&pagesize=15"%page ,verify=False)
    soup = BeautifulSoup(res.text)

    for item in soup.select(".DataTable2 td"):
        print item.text.strip()
        result =open("TWD-USD/TWD-USD.txt",'a')
        result.write(item.text.strip() + "\n")
print "清單產生完畢"
result.close()