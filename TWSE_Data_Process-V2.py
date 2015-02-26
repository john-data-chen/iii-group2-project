# coding=utf-8
# 本程式目的為整理已抓到最新的每日股價資料所需要的欄位後另存新檔
# 改版目的：可讀取0050_ticker_list.csv中的股號，成分股若變動只需改csv，不用改程式
__author__ = 'john.chen'

import os

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWSE_Stocks_Processed"):
    os.mkdir("TWSE_Stocks_Processed")

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
    f = open("TWSE_Stocks/" + ticker + ".txt", "r")   # 讀取format(stock) + 檔名.txt
    new = open("TWSE_Stocks_Processed/" + ticker + ".txt",'w') # 另存新檔

    # 提示現在處理到哪一隻股票
    print "正處理 %s (%d out of %d)" % (ticker, counter, len(file_content))
    # counter + 1
    counter += 1
    for line in f.readlines(): # 讀取每一列
        element = line.strip().split() # 以空白分割每一格資料為每個元素

        # 只留下 日期、成交股數、最高價、最低價、收盤價
        print element[0] + " " + element[1] + " " + element[4] + " " + element[5] + " " + element[6]
        # 以空白字元分隔，寫到最後一個元素要換行\n
        new.write(element[0] + " " + element[1] + " " + element[4] + " " + element[5] + " " + element[6] + "\n")
    # 關閉檔案
    f.close()
    new.close()

print "清單產生完畢"