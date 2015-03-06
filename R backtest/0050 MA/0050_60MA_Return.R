# 本程式目的為分析0050在收盤價突破跟跌破60日均線策略下的報酬率

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
# 60日均線中線交易者常用
a = runMean(as.numeric(priceXts[,6]),n = 60)
names(a)= rownames(priceTab)
ma_60 = as.xts(a)

# 策略回測：當收盤價 > 60ma，全壓；當收盤價 < 60ma，空手
# position為一個時間序列，以日為單位，如果收盤價大於60ma，設值為1；否則設值為0。
# 由於我們是日資料，訊號發生時只能隔天做交易，故將這向量全部往後遞延一天。
position<-Lag(ifelse(priceXts[,6]>ma_60, 1,0))
# ROC計算：log(今天收盤價/昨天收盤價)，乘上poistion代表。若1則持有，若0則空手。
temp<-ROC(Cl(priceTab))*position
# 回測多少時間，可再改
ma60Re<-temp['2004-01-01/2015-02-26']
# cumsum計算累計值，即將每一分量之前的值累加起來。取exp函數是要計算累計報酬率。
ma60Re<-exp(cumsum(temp[!is.na(temp)]))
# 累計報酬率畫出圖表
plot(ma60Re)