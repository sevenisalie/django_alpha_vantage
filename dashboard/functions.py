import requests
import pandas as pd
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import datetime
import time
from pandas import Timestamp
import requests

def spotquote(symbol):
    import requests
    import json
    symbol=symbol
    payload = {
      'symbol': symbol,
    }
    url = 'https://api.binance.us/api/v3/ticker/price'
    r = requests.get(url, params = payload)
    data = r.json()

    return data



#returns a pandas dataframe with candlestick data
def candles(symbol):
  symbol=symbol
  interval = '1m'
  limit = '500'

  payload = {
      'symbol': symbol,
      'interval': interval,
      'limit': limit,
  }

  url= 'https://api.binance.us/api/v3/klines'
  r = requests.get(url, params = payload)
  r = r.json()

  index = []
  open = []
  high = []
  low = []
  close = []
  volume = []
  for i in r:
    index.append(i[:][0])
    open.append(i[:][1])
    high.append(i[:][2])
    low.append(i[:][3])
    close.append(i[:][4])
    volume.append(i[:][5])

  newindex=[]
  for n in index:
      newindex.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(n/1000)))

  ts_df = pd.DataFrame(open,
                       index = newindex,
                       columns=['open'],
                       )
  ts_df['high'] = high
  ts_df['low'] = low
  ts_df['close'] = close
  ts_df['volume'] = volume



  df = ts_df.reindex(index=ts_df.index[::-1])


  return df



 #PRICE CHANGE DATA
def pricechange(symbol):
    symbol=symbol
    payload = {
        'symbol': symbol,
    }
    url= 'https://api.binance.us/api/v3/ticker/24hr'
    r = requests.get(url, params = payload)
    r = r.json()
    pricechange = r
    return pricechange
