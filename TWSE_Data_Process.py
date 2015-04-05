# coding=utf-8
# 撰寫人：陳建安 (John Chen) 聯絡信箱：john.data.chen@facebook.com
# 本程式目的為整理已抓到最新的每日股價資料所需要的欄位後另存新檔

import os

# 要是沒有這個資料夾，新建一個
if not os.path.exists("TWSE_Stocks_Processed"):
    os.mkdir("TWSE_Stocks_Processed")

# 股票代碼表，按照順序重排
group = ['0050','1101','1102','1216','1301','1303','1326',\
         '1402','2002','2105','2207','2227','2301','2303',\
         '2308','2311','2317','2325','2330','2354','2357',\
         '2382','2395','2408','2409','2412','2454','2474',\
         '2498','2801','2880','2881','2882','2883','2884',\
         '2885','2886','2887','2890','2891','2892','2912',\
         '3008','3045','3474','3481','4904','4938','5880',\
         '6505','9904']

for stock in group: # 每個代碼新建一個txt
    f = open("TWSE_Stocks/" + format(stock) + "_bid_detail.txt", "r")   # 讀取format(stock) + 檔名.txt
    new = open("TWSE_Stocks_Processed/" + format(stock) + "_bid_detail.txt",'w') # 另存新檔

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