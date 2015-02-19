# coding=utf-8
# 本程式目的為抓取標準普爾指數ETF：SPY及其502支成分股每日的股價資料
__author__ = 'john.chen'

import time, os
import urllib2

# 假如沒有這個資料夾就新增
if not os.path.exists("SPY_stocks"):
    os.mkdir("SPY_stocks")

"""
必須修改網頁中的標頭，來下載想要的日期，以下為網址註解：
s = 股票代碼，定義在SPY_list.csv裡面，要改的是csv
a = fromMonth-1
b = fromDay (兩位數，1~9前要加0)
c = fromYear
d = toMonth-1
e = toDay (兩位數，1~9前要加0)
f = toYear
"""
url_part1 = 'http://ichart.finance.yahoo.com/table.csv?s='
url_part2 = '&d=1&e=18&f=2015&g=d&a=0&b=01&c=2004&ignore=.csv'

# 新增全域變數給檔案處理
global f
# 讀取成分股列表
f = open('SPY_stocks/SPY_list.csv', 'r')
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
        history_file = open("SPY_stocks/" + ticker + ".csv", "w")
        history_file.write(response.read())
        history_file.close()
        # 休眠 3secs
        time.sleep(3)

    except Exception, e:
        pass

# 提示結束並關檔
print "所有清單下載完畢"
f.close()