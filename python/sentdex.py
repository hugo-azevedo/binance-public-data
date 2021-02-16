import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web

style.use('ggplot')

df = pd.read_csv('./data/spot/klines/1INCHBTC/1h/1INCHBTC-1h-2020-12.csv',
  index_col=0,
  names=[ 'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 
          'Quote asset volume', 'Number of trades',
          'Taker buy base asset volume', 'Taker buy quote asset volume', 
          'Ignore']
)
print(df.head())