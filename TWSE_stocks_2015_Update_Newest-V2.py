#! coding=UTF-8
# 本程式目的為抓取證交所0050及其成分股共51支股票從2015年最新的單日股價資料
# 改版目的：可讀取0050_ticker_list.csv中的股號，成分股若變動只需改csv，不用改程式
__author__ = 'john.chen'

import requests, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWSE_Stocks"):
    os.mkdir("TWSE_Stocks")

# 新增全域變數給檔案處理
global f
# 讀取成分股列表
f = open('TWSE_Stocks/list/0050_ticker_list.csv', 'r')
# 讀取有幾列，代表有幾支成分股
file_content = f.readlines()
# counter從1開始
counter = 1;

# 印出file_content後發現'3474\n'每個元素後都有換行符號 \n，這會造成寫檔錯誤
#print file_content

for ticker in file_content:
    # 將代號後面的換行符號 \n 去掉
    ticker = ticker.strip()
    # 每個代碼新建一個txt
    bid_detail = open("TWSE_Stocks/" + ticker + ".txt",'w')
    # 提示現在下載到哪一隻股票
    print "正下載 %s (%d out of %d)" % (ticker, counter, len(file_content))
    # counter + 1 = 下一隻股票
    counter += 1

    for year in range(2015,2016): # 2015年
        for a in range(3,4): # 現在是3月
            if a < 10: # 如果是1~9月前面加0，01~09
                month = "0" + str(a)
            else:
                month = a # 10以上就原樣輸出

            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report{}{}/{}{}_F3_1_8_{}.php?STK_NO={}&myear={}&mmon={}#"
            res = requests.get(url.format(year,month,year,month,ticker,ticker,year,month)) # {}放參數的意思，year：年，month：月，stock：股票代號
            # print res.encoding # 找出網頁編碼
            soup = BeautifulSoup(res.text.encode('ISO-8859-1'))

            counter2 = 0
            # 如果需要表頭，將以下整個for迴圈複製，然後改為for i in soup.select(".basic2 td")[0:9]:
            # 然後將新的迴圈貼在這個迴圈前面。
            for i in soup.select(".basic2 td")[-9:-1:]: # 只抓最後9個元素
                bid_detail.write(i.text.strip().encode('utf-8') + " "), # 每次寫入時以空白隔開, ","代表連續寫不換行
                print i.text,
                counter2 += 1 # 每寫一格，counter2 + 1
                if counter2 == 9: # 當寫到第9格的時候代表該換行了
                    bid_detail.write("\n"), # 換行
                    print ""
                    counter2 = 0 # 歸零重來
            # 換行分隔
            print ""

# 提示結束, 關閉寫檔
print "清單產生完畢"
bid_detail.close()
f.close()