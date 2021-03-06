#! coding=UTF-8
# 撰寫人：陳建安 (John Chen) 聯絡信箱：john.data.chen@facebook.com
# 所0050及其成分股共51支股票從2015年最新的單日股價資料

import requests, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWSE_Stocks"):
    os.mkdir("TWSE_Stocks")

# 股票代碼表，按照順序重排
group = ['0050','1101','1102','1216','1301','1303','1326',\
         '1402','2002','2105','2207','2227','2301','2303',\
         '2308','2311','2317','2325','2330','2354','2357',\
         '2382','2395','2408','2409','2412','2454','2474',\
         '2498','2801','2880','2881','2882','2883','2884',\
         '2885','2886','2887','2890','2891','2892','2912',\
         '3008','3045','3474','3481','4904','4938','5880',\
         '6505','9904']

for stock in group:   # 每個代碼新建一個txt
    bid_detail=open("TWSE_Stocks/" + format(stock) + "_bid_detail.txt",'w')
    print "現在處理的是" + stock
    for year in range(2015,2016): # 2015年
        for a in range(4,5): # 現在是4月
            if a < 10: # 如果是1~9月前面加0，01~09
                month = "0" + str(a)
            else:
                month = a # 10以上就原樣輸出

            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report{}{}/{}{}_F3_1_8_{}.php?STK_NO={}&myear={}&mmon={}#"
            res = requests.get(url.format(year,month,year,month,stock,stock,year,month)) # {}放參數的意思，year：年，month：月，stock：股票代號
            # print res.encoding # 找出網頁編碼
            soup = BeautifulSoup(res.text.encode('ISO-8859-1'))

            counter = 0
            # 如果需要表頭，將以下整個for迴圈複製，然後改為for i in soup.select(".basic2 td")[0:9]:
            # 然後將新的迴圈貼在這個迴圈前面。
            for i in soup.select(".basic2 td")[-10:-1]: # 只抓最後9個元素
                bid_detail.write(i.text.strip().encode('utf-8') + " "), # 每次寫入時以空白隔開, ","代表連續寫不換行
                print i.text,
                counter += 1 # 每寫一格，counter + 1
                if counter == 9: # 當寫到第9格的時候代表該換行了
                    bid_detail.write("\n"), # 換行
                    print ""
                    counter = 0 # 歸零重來
            print ""

# 提示結束, 關閉寫檔
print "清單產生完畢"
bid_detail.close()
