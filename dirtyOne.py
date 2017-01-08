import quandl
import pandas as pd
import numpy as np
import time

#quandl.ApiConfig.api_key = "MyYX3VZfZ4xPeJ1jza9D"
#tok = "MyYX3VZfZ4xPeJ1jza9D"

#Getting the fundamentals data
df = pd.read_csv("Fundamentals/SF0_20170108.csv",header=None)
df.columns = ['label','date','value']

#wee bit of cleanup on the labels
dfTemp = pd.DataFrame(df['label'].str.split('_').tolist(),columns=['ticker','attributes','MRY'])
df['ticker'],df['attributes'] = dfTemp['ticker'],dfTemp['attributes']
df = df.drop("label",axis=1)
#reset_selective(dfTemp);y

#extracting the months and years out of dates and dropping the latter
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df = df.drop('date',axis=1)

#loading up the historical price data
prices = pd.read_csv('Fundamentals/WIKI_PRICES_212b326a081eacca455e13140d7bb9db.csv',usecols=['ticker','date','adj_close'])
prices['date'] = pd.to_datetime(prices['date'])
prices['year'] = prices['date'].dt.year
prices['month'] = prices['date'].dt.month

#averaging the prices of the fiscal year-end month
avgP = prices.groupby(['ticker','year','month'],as_index=False).mean()

#Calculating returns per ticker
prices = prices.set_index('date')
prices_shrt = prices[prices['year']>2011]
prices_shrt['return'] = 1.0
prices_shrt['return'] = prices_shrt.groupby(['ticker', 'year']).pct_change()
prices_shrt['return'] = prices_shrt['return'] + 1
prices_shrt.groupby(by='ticker')['return'].prod()
prices_shrt['return'] = prices_shrt['return'] - 1



fif = prices_shrt.head(n=10000)
#calculating returns for every stock
%%time
fif['return'] = 1.0
for i in range(0,len(fif)):
    if fif['ticker'][i-1] == fif['ticker'][i]:
        fif['return'][i] = fif["adj_close"][i]/fif["adj_close"][i-1]
    else:
        0.0
prices_shrt['return'] + 1 
prices_shrt.groupby(by='ticker')['return'].prod()

#too long
#EXPLORE OPTION 2, FOR LOOPING EVERY TICKER AND USING SHIFT(1) METHOD!!!!!!!

prices_shrt['return'] = 1.0
%%time
for i in range(0,len(prices_shrt)):
    if prices_shrt['ticker'][i-1] == prices_shrt['ticker'][i]:
        prices_shrt['return'][i] = prices_shrt["adj_close"][i]/prices_shrt["adj_close"][i-1]
    else:
        0.0
pd.write_csv(prices_shrt,"returns.csv")
fif.groupby(by='ticker')['return'].prod()


#http://stackoverflow.com/questions/40273251/pandas-groupby-with-pct-change
fif['return'] = fif.groupby(['ticker', 'year']).pct_change()
prices_shrt['return'] = prices_shrt.groupby(['ticker', 'year']).pct_change()


fuit = df.groupby(['ticker','year','month'],as_index=False).count()
fuit['attributes'] = 'price'
fuit = pd.merge(fuit,avgP, on = ['ticker','year','month'], how='left')
fuit = fuit.drop(['value'],axis=1)
fuit.columns = ['ticker','year','month','attributes','value']
df = df.append(fuit)

#drop the NaN
df = df[np.isfinite(df['value'])]


#fuit.groupby(['ticker'],as_index=False).max()/fuit.groupby(['ticker'],as_index=False).min()

#freeing up some RAM
#reset_selective(fuit)
reset_selective(f)


#CFO = df.loc[df['Attributes']=='NCFO']
