#! coding:utf-8
import requests
import time
from bs4 import BeautifulSoup
import os

if not os.path.exists("TWSE_history"):
    os.mkdir("TWSE_history")

for i in range(101,103):   # 跑101~103年
    for j in range(1,13):  # 跑1-12月份
        time.sleep(3)
        if j < 10:     # 處理網頁月份問題01~09
            month = '0' + str(j)    # 月份01~09
        else:
            month = j
        payload = {
                'myear':'%d'%i,      # %d 整數
                'mmon':'%s'%month    # %s 字串
        }
        fid=open('TWSE_history/test.txt','w')
        fid.write('"日期","開盤指數","最高指數","最低指數","收盤指數"\n') # 用' ' 把他變成一個字串
        user_post=requests.post('http://www.twse.com.tw/ch/trading/indices/MI_5MINS_HIST/MI_5MINS_HIST.php',data=payload)
        user_post.encoding="big5"
        soup=BeautifulSoup(user_post.text)
        for td in soup.select(".board_trad tr")[2:]:    # td為變數可隨便取。從文件裡面取得所有的連結，board_trad是table class。select(".board_trad tr td，裡面可內多個條件，要加"空格")
            fid=open('TWSE_history/test.txt','a')
            print td.text.strip()                       # [2:]  去頭，從網頁第二起的資料到結束都要
            fid.write(td.text.strip() +"\n")             # +"\n斷行"
        fid.close()
        print "清單產生完畢"