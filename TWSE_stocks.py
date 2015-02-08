#! coding=UTF-8
import requests
from bs4 import BeautifulSoup

group = ['3607']

for i in range(2014,2013,-1): # 2014年 = 民國103年
    for j in range(1,13): # 1~12月
        year = i
        if j < 10: # 如果是1~9月前面加0，01~09
            month = "0" + str(j)
        else:
            month = j # 10以上就原樣輸出
        for stock in group:   # 跑股票代碼
            bid_detail=open(format(stock) + "_bid_detail.txt",'a') # 改成format(stock) + 檔名.txt，模式改為'a' = 附加模式
            url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY_AVG/genpage/Report{}{}/{}{}_F3_1_8_{}.php?STK_NO={}&myear={}&mmon={}#"
            res = requests.get(url.format(year,month,year,month,stock,stock,year,month))     # {}放參數的意思，year：年，month：月，stock：股票代號
            # print res.encoding # 網頁編碼
            soup = BeautifulSoup(res.text.encode('ISO-8859-1'))
            for td in soup.select(".board_trad tr"):    # .board_trad .是select的用方
                bid_detail.write(td.text.encode('utf-8')+'\n')
                print td.text
bid_detail.close()