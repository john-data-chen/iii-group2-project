# 本程式目的為分析0050在均線黃金與死亡交叉策略下的報酬率

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
# 10日均線強勢股交易者常用
a = runMean(as.numeric(priceXts[,6]),n = 10)
names(a)= rownames(priceTab)
ma_10 = as.xts(a)
# 20日均線短線交易者常用
a = runMean(as.numeric(priceXts[,6]),n = 20)
names(a)= rownames(priceTab)
ma_20 = as.xts(a)

# 策略回測：當10ma > 20ma，全壓；當10ma < 20ma，空手
# position為一個時間序列，以日為單位，如果10ma大於20ma，設值為1；否則設值為0。
# 由於我們是日資料，訊號發生時只能隔天做交易，故將這向量全部往後遞延一天。
position<-Lag(ifelse(ma_10>ma_20, 1,0))
# ROC計算：log(今天收盤價/昨天收盤價)，乘上poistion代表。若1則持有，若0則空手。
temp<-ROC(Cl(priceTab))*position
# 回測多少時間，可再改
ma10And20<-temp['2004-01-01/2015-02-26']
# cumsum計算累計值，即將每一分量之前的值累加起來。取exp函數是要計算累計報酬率。
ma10And20<-exp(cumsum(temp[!is.na(temp)]))
# 累計報酬率畫出圖表
plot(ma10And20)