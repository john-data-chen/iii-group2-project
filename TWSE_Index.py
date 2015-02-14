#! coding:utf-8
# 本程式目的為抓取台股大盤指數
import requests
import time
from bs4 import BeautifulSoup
import os

if not os.path.exists("TWSE_index"):
    os.mkdir("TWSE_index")

fid = open('TWSE_index/index.txt','w') # 寫入檔案
for year in range(101,103):   # 跑101~103年
    for a in range(1,13):  # 跑1-12月份
        time.sleep(3)
        if a < 10:     # 處理網頁月份問題01~09
            month = '0' + str(a)    # 月份01~09
        else:
            month = a

        payload = {
                'myear':'%d'%year,   # %d 整數
                'mmon':'%s'%month    # %s 字串
        }

        # 只有第1年1月要有表頭，其他月都必須去掉
        if year == 101 and a == 1:
            fid.write('日期 開盤指數 最高指數 最低指數 收盤指數 \n') # 寫入表頭
        user_post = requests.post('http://www.twse.com.tw/ch/trading/indices/MI_5MINS_HIST/MI_5MINS_HIST.php',data=payload)
        user_post.encoding = "big5"
        soup = BeautifulSoup(user_post.text)

        # td為變數可隨便取。從文件裡面取得所有的連結，board_trad是table class。select(".board_trad tr td)，裡面可有多個條件，以"空格"隔開)
        for td in soup.select(".board_trad tr")[2:]:   # [2:]  去頭，從第二行開始留下
            print td.text.strip()
            fid.write(td.text.encode('utf-8').strip() + "\n")    # 寫一行後就"\n斷行"

# 關閉寫入跟提示完成
fid.close()
print "清單產生完畢"