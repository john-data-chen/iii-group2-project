# 本程式目的為分析QQQ在收盤價突破與跌破均線策略下的報酬率

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
# 輸入回測的起點時間，格式：2009-01-01
fromDate = readline()
backtestTime <- priceTab[rownames(priceTab) > fromDate,]
# 去掉NULL
backtestTime$Date = NULL
# 轉換為xts
priceXts = as.xts(backtestTime)

# 載入quantmod，會一起載入TTR
library(quantmod)

# 輸入均線的天數，這個值會是字元，必須as.numeric才能用
maDay = readline()
# 計算均線，收盤價放在第4行
a = runMean(as.numeric(priceXts[,4]),n = as.numeric(maDay))
names(a)= rownames(backtestTime)
ma = as.xts(a)

# 策略回測：當收盤價 > ma，全壓；當收盤價 < ma，空手
# position為一個時間序列，以日為單位，如果收盤價大於ma，設值為1；否則設值為0。
# 由於我們是日資料，訊號發生時只能隔天做交易，故將這向量全部往後遞延一天。
position <- Lag(ifelse(priceXts[,4] > ma, 1,0))
# ROC計算：log(今天收盤價/昨天收盤價)，乘上poistion代表。若1則持有，若0則空手。
maReturn <- ROC(Cl(backtestTime))*position
# cumsum計算累計值，即將每一分量之前的值累加起來。取exp函數是要計算累計報酬率。
maReturn<- exp(cumsum(maReturn[!is.na(maReturn)]))

# 顯示回測起點日期
fromDate
# 顯示均線天數
maDay
# 顯示從起點開始，總共有幾個交易日
length(rownames(backtestTime))
# 計算總共交易幾次，交易次數越多，要付出手續費跟稅就越高
tradeTotal = sum(position -  Lag(position,1) !=0, na.rm=TRUE)
tradeTotal
# 累計報酬率畫出圖表
plot(maReturn)