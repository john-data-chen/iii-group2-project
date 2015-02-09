#! coding=UTF-8
__author__ = 'john.chen'

import requests, time, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWSE_Stocks"):
    os.mkdir("TWSE_Stocks")

# 股票代碼表
group = ['0050','4938','3481','2330','2303','2882','2357','1303','2883',\
         '1301','2002','2311','2317','1402','2892','2880','2801','1216',\
         '1101','1102','2382','2308','1326','2886','2891','2325','2105',\
         '2395','2408','2412','2409','2207','2301','9904','2912','2354',\
         '2474','3045','2454','2881','2887','4904','2885','3008','2498',\
         '2884','2890','6505','5880','2227','3474']

for stock in group:   # 每個代碼新建一個txt
    bid_detail=open("TWSE_Stocks/" + format(stock) + "_bid_detail.txt",'w') # 改成format(stock) + 檔名.txt
    for year in range(2013,2014): # 2014年 - 1911 = 民國103年
        for a in range(1,13): # 1~12月
            if a < 10: # 如果是1~9月前面加0，01~09
                month = "0" + str(a)
            else:
                month = a # 10以上就原樣輸出

            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report{}{}/{}{}_F3_1_8_{}.php?STK_NO={}&myear={}&mmon={}#"
            res = requests.get(url.format(year,month,year,month,stock,stock,year,month)) # {}放參數的意思，year：年，month：月，stock：股票代號
            # print res.encoding # 找出網頁編碼
            soup = BeautifulSoup(res.text.encode('ISO-8859-1'))

            counter = 0
            for i in soup.select(".basic2 td"): # 更改標籤
                bid_detail.write(i.text.strip().encode('utf-8') + " "), # 每次寫入時以空白隔開, ","代表連續寫不換行
                print i.text,
                counter += 1 # 每寫一格，counter + 1
                if counter == 9: # 當寫到第9格的時候代表該換行了
                    bid_detail.write("\n"), # 換行
                    print ""
                    counter = 0 # 歸零重來
                    # 日期 成交股數...這表頭每個月前頭都會出現一次，是可以手動刪除，但為了之後方便，應該要改

# 提示結束, 關閉寫檔, delay
print "清單產生完畢"
bid_detail.close()
time.sleep(5)