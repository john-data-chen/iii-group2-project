#! coding=UTF-8
# 本程式目的為抓取證交所0050及其成分股共51支股票從2004~2014年每日的股價資料
# 改版目的：可讀取0050_ticker_list.csv中的股號，成分股若變動只需改csv，不用改程式
# 2015年的資料請改用2015_append.py 抓最新的月資料，2015_update_newest是最新的日資料
__author__ = 'john.chen'

import requests, time, os
from bs4 import BeautifulSoup

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWSE_Stocks"):
    os.mkdir("TWSE_Stocks")

# 新增全域變數給檔案處理
global f
# 讀取成分股列表
f = open('TWSE_Stocks/0050_ticker_list.csv', 'r')
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
    for year in range(2004,2015): # 2014年 - 1911 = 民國103年, 日期：2004~2014
        for a in range(1,13): # 1~12月
            if a < 10: # 如果是1~9月前面加0，01~09
                month = "0" + str(a)
            else:
                month = a # 10以上就原樣輸出

            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report{}{}/{}{}_F3_1_8_{}.php?STK_NO={}&myear={}&mmon={}#"
            res = requests.get(url.format(year,month,year,month,ticker,ticker,year,month)) # {}放參數的意思，year：年，month：月，stock：股票代號
            # print res.encoding # 找出網頁編碼
            soup = BeautifulSoup(res.text.encode('ISO-8859-1'))

            # 只有第1年1月要有表頭：日期 成交股數...etc，其他月都必須去掉
            if year == 2004 and a == 1:
                index = 0 # 要抓表頭
            else:
                index = 9 # 去掉表頭

            counter2 = 0
            for i in soup.select(".basic2 td")[index:]: # index控制表頭的抓下或去除
                bid_detail.write(i.text.strip().encode('utf-8') + " "), # 每次寫入時以空白隔開, ","代表連續寫不換行
                print i.text,
                counter2 += 1 # 每寫一格，counter2 + 1
                if counter2 == 9: # 當寫到第9格的時候代表該換行了
                    bid_detail.write("\n"), # 換行
                    print ""
                    counter2 = 0 # 歸零重來

            # 休眠
            time.sleep(3)

# 提示結束, 關閉寫檔
print "清單產生完畢"
bid_detail.close()
f.close()