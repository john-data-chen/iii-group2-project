# 本程式目的為分析0050在收盤價突破跟跌破240日均線策略下的報酬率

# 載入RODBC
library(RODBC)
# ODBC 名稱/ user / password
conn <- odbcConnect("mysql", uid="root", pwd="")
# 讀取table
sqlTables(conn)
# 讀取table 0050
priceTab<-sqlFetch(conn,"0050")

# 關閉連線
close(conn)

# 載入xts
library(xts)
# rownames = date
rownames(priceTab) = priceTab[,1]
# 去掉NULL
priceTab$Date = NULL
# 轉換為xts
priceXts = as.xts(priceTab)

# 載入quantmod
library(quantmod)

# 定義均線
# 收盤價放在第6行
# 240日均線是長線，一般很少用，僅作為比較參考
a = runMean(as.numeric(priceXts[,6]),n = 240)
names(a)= rownames(priceTab)
ma_240 = as.xts(a)

# 策略回測：當收盤價 > 240ma，全壓；當收盤價 < 240ma，空手
# position為一個時間序列，以日為單位，如果收盤價大於240ma，設值為1；否則設值為0。
# 由於我們是日資料，訊號發生時只能隔天做交易，故將這向量全部往後遞延一天。
position<-Lag(ifelse(priceXts[,6]>ma_240, 1,0))
# ROC計算：log(今天收盤價/昨天收盤價)，乘上poistion代表。若1則持有，若0則空手。
temp<-ROC(Cl(priceTab))*position
# 回測多少時間，可再改
ma240Re<-temp['2004-01-01/2015-02-26']
# cumsum計算累計值，即將每一分量之前的值累加起來。取exp函數是要計算累計報酬率。
ma240Re<-exp(cumsum(temp[!is.na(temp)]))
# 累計報酬率畫出圖表
plot(ma240Re)