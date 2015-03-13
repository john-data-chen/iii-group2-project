# coding= utf-8
# 本程式目的為抓取0050成分股代號並列成清單
__author__ = 'john.chen'

import requests, os
from bs4 import BeautifulSoup

# 假如沒有這個資料夾就新增
if not os.path.exists("TWSE_stocks"):
    os.mkdir("TWSE_stocks")

res = requests.get("http://www.twse.com.tw/ch/trading/indices/twco/tai50i.php", verify = False)
# 找出網頁編碼
#print res.encoding
soup = BeautifulSoup(res.text.encode("ISO-8859-1"))

# 將所有資料先存成0050_list_total.csv
total = open("TWSE_Stocks/list/0050_data_list.csv",'w')
# 寫入表頭
print "代號" + " " + "名稱" + " " + "ICB行業分類指標" + " " + "發行股數(單位:股)" + " " + "公眾流通量係數" + " " + "占臺灣50指權重"
total.write("代號" + " " + "名稱" + " " + "ICB行業分類指標" + " " + "發行股數(單位:股)" + " " + "公眾流通量係數" + " " + "占臺灣50指權重" + "\n")
# 新增計數器
counter = 0
for td in soup.select(".tb2 td"):
    print td.text.strip(),
    total.write(td.text.strip().encode('utf-8') + " ")
    # 每印一格，計數器 +1
    counter += 1
    # 每印六格就要換行
    if counter == 6:
        print ""
        total.write("\n")
        # 計數器歸零
        counter = 0
# 提示結束，關閉寫檔
print "0050 成分股所有資料已寫入0050_list_total.csv"
print ""
total.close()

# 讀取之前寫入的清單，處理後只留下股號，存入新檔
new = open("TWSE_Stocks/list/0050_ticker_list.csv",'w')
open = open("TWSE_Stocks/list/0050_data_list.csv",'r')
print "處理成分股清單後只留下股號，存入新檔"

# 這個迴圈，會將每列的格子存入一個個元素裡
for line in open.readlines()[1:]: # 從1開始是為了去掉表頭
    element = line.strip().split()
    # 只留下股號
    print element[0]
    new.write(element[0] + "\n")

# 提示結束，關閉寫檔
print "0050 成分股所有股號已寫入0050_ticker_list.csv"
open.close()
new.close()