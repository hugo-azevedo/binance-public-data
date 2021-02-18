import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web

style.use('ggplot')

df = pd.read_csv('./data/csv/1INCHBTC-1h-2020-12.csv', index_col=0, names= [
  'start', 'open', 'high', 'low', 'close', 'volume', 'end', 
  'qav', # Quote asset volume
  'trades', # Number of trades
  'tbbav', # Taker buy base asset volume
  'tbqav', # Taker buy quote asset volume
  'ignore'
])
df = df.drop(columns=['qav', 'tbbav', 'tbqav', 'ignore'])
df.index = pd.to_datetime(df.index, unit='ms')
df['end'] = pd.to_datetime(df['end'], unit='ms')

print(df.head())

ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['close'])
ax2.bar(df.index, df['volume'])

plt.show()