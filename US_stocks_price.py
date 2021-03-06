# coding=utf-8
# 撰寫人：陳建安 (John Chen) 聯絡信箱：john.data.chen@facebook.com
# 本程式目的為抓取美股每日的股價資料

import time, os
import urllib2

# 假如沒有這個資料夾就新增
if not os.path.exists("US_stocks_price"):
    os.mkdir("US_stocks_price")

"""
必須修改網頁中的標頭，來下載想要的日期，以下為網址註解：
s = 股票代碼，定義在ticker_list.csv裡面，csv格式必須如下：
DIA
AAPL
AMZN
....

a = fromMonth-1
b = fromDay (兩位數，1~9前要加0)
c = fromYear
d = toMonth-1
e = toDay (兩位數，1~9前要加0)
f = toYear
"""
url_part1 = 'http://ichart.finance.yahoo.com/table.csv?s='
url_part2 = '&d=3&e=05&f=2015&g=d&a=0&b=01&c=2009&ignore=.csv'

# 新增全域變數給檔案處理
global f
# 讀取成分股列表，路徑與檔名參考下行
f = open('US_stocks_price/list/ticker_list.csv', 'r')
# 讀取有幾列，代表有幾支成分股
file_content = f.readlines()
# counter從1開始
counter = 1;
# 提示有幾隻股票要下載
print "總共有 %d 股票的資料會被下載" % len(file_content)

# 讀取股票代號
for ticker in file_content:
    ticker = ticker.strip()
    # 重組成完整網址
    url = url_part1 + ticker + url_part2

    try:
        # 這會造成404 exception
        response = urllib2.urlopen(url)
        # 提示現在下載哪一隻股票
        print "正下載 %s (%d out of %d)" % (ticker, counter, len(file_content))

        # 完成後 counter + 1
        counter = counter + 1

        # 股價寫入新檔
        history_file = open("US_stocks_price/" + ticker + ".csv", "w")
        history_file.write(response.read())
        history_file.close()
        # 休眠 3secs
        time.sleep(3)

    except Exception, e:
        pass

# 提示結束並關檔
print "所有清單下載完畢"
f.close()