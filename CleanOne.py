import quandl
import pandas as pd
import numpy as np
import time

#Getting the fundamentals data
df = pd.read_csv("Fundamentals/SF0_20170108.csv",header=None)
df.columns = ['label','date','value']

#wee bit of cleanup on the labels
dfTemp = pd.DataFrame(df['label'].str.split('_').tolist(),columns=['ticker','attributes','MRY'])
df['ticker'],df['attributes'] = dfTemp['ticker'],dfTemp['attributes']
df = df.drop("label",axis=1)


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
prices_shrt['value'] = 1.0
prices_shrt['value'] = prices_shrt.groupby(['ticker', 'year','month']).pct_change()
prices_shrt['value'] = prices_shrt['value'] + 1
monthlyR = prices_shrt.groupby(by=['ticker','year','month'],as_index=False)['value'].prod()
monthlyR['value'] = monthlyR['value'] -1
monthlyR['attributes'] = 'monthlyReturn'
df = df.append(monthlyR)


#average year-end prices
fuit = df.groupby(['ticker','year','month'],as_index=False).count()
fuit['attributes'] = 'price'
fuit = pd.merge(fuit,avgP, on = ['ticker','year','month'], how='left')
fuit = fuit.drop(['value'],axis=1)
fuit.columns = ['ticker','year','month','attributes','value']

#appending the calculated data to the master dataframe
df = df.append(fuit)

#drop the NaN
df = df[np.isfinite(df['value'])]

#fuit.groupby(['ticker'],as_index=False).max()/fuit.groupby(['ticker'],as_index=False).min()

#freeing up some RAM
#reset_selective(fuit)
reset_selective(f)


#CFO = df.loc[df['Attributes']=='NCFO']
