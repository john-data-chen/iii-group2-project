# 撰寫人：陳建安 (John Chen) 聯絡信箱：john.data.chen@facebook.com
# 本程式目的為分析QQQ在均線2條線交叉策略下的報酬率

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

# 輸入第1條線的天數，天數必須是較短的，這個值會是字元，必須as.numeric才能用
shortDay = readline()
# 計算短天數均線，收盤價放在第4行
a = runMean(as.numeric(priceXts[,4]),n = as.numeric(shortDay))
names(a)= rownames(backtestTime)
maShort = as.xts(a)

# 輸入第2條線的天數，天數必須是較長的
longDay = readline()
# 計算長天數均線
a = runMean(as.numeric(priceXts[,4]), n = as.numeric(longDay))
names(a)= rownames(backtestTime)
maLong = as.xts(a)

# 策略回測：當短天數ma > 長天數ma，全壓；當短天數ma < 長天數ma，空手
# position為一個時間序列，以日為單位，如果短天數ma大於長天數ma，設值為1；否則設值為0。
# 由於我們是日資料，訊號發生時只能隔天做交易，故將這向量全部往後遞延一天。
position <- Lag(ifelse(maShort > maLong, 1,0))
# ROC計算：log(今天收盤價/昨天收盤價)，乘上poistion代表。若1則持有，若0則空手。
maReturn <- ROC(Cl(backtestTime))*position
# cumsum計算累計值，即將每一分量之前的值累加起來。取exp函數是要計算累計報酬率。
maReturn<- exp(cumsum(maReturn[!is.na(maReturn)]))

# 顯示回測起點日期
fromDate
# 顯示短天數跟長天數的參數
shortDay
longDay
# 顯示從起點開始，總共有幾個交易日
length(rownames(backtestTime))
# 計算總共交易幾次，交易次數越多，要付出手續費跟稅就越高
tradeTotal = sum(position -  Lag(position,1) !=0, na.rm=TRUE)
tradeTotal

# 轉換xts成data.frame
df_return = as.data.frame(maReturn)
df_return = data.frame(date = rownames(df_return), return = df_return$Lag.1, row.names=NULL)
# 把所有自訂參數接在一起，方便命名
fileName = paste(shortDay, longDay, fromDate, sep=",")
# 另存成csv
write.table(df_return, file =sub("%s", fileName, "QQQ_MA_%s.csv"), sep = ",", col.names = NA)

# 累計報酬率畫出圖表
plot(maReturn)
