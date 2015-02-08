#!encode=utf-8
# 參考https://gist.github.com/ywchiu/d726e0d042031a10bf10

import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from dateutil.relativedelta import relativedelta

getyear =  dt.split('/',1)
bctime =  str(int(getyear[0]) + 1911) +"/"+ getyear[1]
for i in range(1,10):
    ts =  (datetime.strptime(bctime, "%Y/%m") - relativedelta(months=i)).strftime("%Y/%m")
    ts2 = ts.split('/',1)
    ts3 = str(int(ts2[0]) - 1911) + '/' + ts2 [1]

        payload = {
            'report1':'day',
            'input_date':'104%2F{}%2F{}'.format(month,day),
            'mSubmit':'%ACd%B8%DF',
            'yr':'2015',
            'w_date':'20150126',
            'm_date':'20150101',
        }
        res = requests.post("http://www.twse.com.tw/ch/trading/fund/BFI82U/BFI82U.php",data = payload)

        res.encoding = "big5"
        soup = BeautifulSoup(res.text)

        for td in soup.select(".board_trad tr"):
            print td.text.strip()