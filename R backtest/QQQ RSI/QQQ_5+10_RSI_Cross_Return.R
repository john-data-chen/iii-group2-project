# 本程式目的為分析QQQ在RSI(5,10)交叉策略下的報酬率

# 載入RODBC
library(RODBC)
# ODBC 名稱/ user / password
conn <- odbcConnect("mysql", uid="root", pwd="")
# 讀取table
sqlTables(conn)
# 讀取table qqq
priceTab <- sqlFetch(conn,"qqq")
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

# 載入quantmod，會一起載入TTR
library(quantmod)

# 計算RSI5
a = RSI(as.numeric(priceXts[,4]), n = 5)
names(a)= rownames(priceTab)
rsi5 = as.xts(a)
# 計算RSI10
a = RSI(as.numeric(priceXts[,4]), n = 10)
names(a)= rownames(priceTab)
rsi10 = as.xts(a)

# 策略回測：當rsi5 > rsi10，全壓；當rsi5 < rsi10，空手
# position為一個時間序列，以日為單位，如果rsi5大於rsi10，設值為1；否則設值為0。
# 由於我們是日資料，訊號發生時只能隔天做交易，故將這向量全部往後遞延一天。
position <- Lag(ifelse(rsi5 > rsi10, 1,0))
# ROC計算：log(今天收盤價/昨天收盤價)，乘上poistion代表。若1則持有，若0則空手。
temp <- ROC(Cl(priceTab))*position
# 回測多少時間，可再改
rsi5And10 <- temp['2004-01-01/2015-02-26']
# cumsum計算累計值，即將每一分量之前的值累加起來。取exp函數是要計算累計報酬率。
rsi5And10 <- exp(cumsum(temp[!is.na(temp)]))
# 累計報酬率畫出圖表
plot(rsi5And10)
