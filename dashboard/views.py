from django.shortcuts import render

#for financial data api
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import datetime
from pandas import Timestamp
import requests

# Create your views here.

def homeView(request):


    api_key = 'YX9741BHQFXIYA0B'

    stock = 'INTC'

    api_key = 'YX9741BHQFXIYA0B'
    period= 60

    ts = TimeSeries(key=api_key, output_format='pandas',)
    data_ts, meta_data_ts = ts.get_intraday(stock, interval='1min', outputsize='compact')

    ti = TechIndicators(key=api_key, output_format='pandas')
    data_ti, meta_data_ti  = ti.get_rsi(stock, interval='1min', time_period=period, series_type='close')

    ts_df = data_ts
    ti_df = data_ti

    #Fundamentals
    payload = {'function': 'OVERVIEW', 'symbol': 'INTC', 'apikey': 'YX9741BHQFXIYA0B'}
    r = requests.get('https://www.alphavantage.co/query', params=payload)
    r = r.json()


    #plotly graph
    def candlestick():
        figure = go.Figure(
            data = [
                    go.Candlestick(
                      x = ts_df.index,
                      high = ts_df['2. high'],
                      low = ts_df['3. low'],
                      open = ts_df['1. open'],
                      close = ts_df['4. close'],
                    )
                  ]
        )

        candlestick_div = plot(figure, output_type='div')
        return candlestick_div


    sector = r['Sector']
    marketcap = r['MarketCapitalization']
    peratio = r['PERatio']
    yearhigh = r['52WeekHigh']
    yearlow = r['52WeekLow']
    eps = r['EPS']



    timeseries = ts_df.to_dict(orient='records')

    closingprice = []
    for k in timeseries:
      closingprice.append(k['4. close'])

    #miscellaneous stuff
    day = datetime.datetime.now()
    day = day.strftime("%A")

    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    marketcap = int(marketcap)
    marketcap = human_format(marketcap)

    closingprice = closingprice[0:15]


    context = {
        'sector': sector,
        'marketcap': marketcap,
        'peratio': peratio,
        'yearhigh': yearhigh,
        'yearlow': yearlow,
        'eps': eps,
        'closingprice': closingprice,
        'timeseries': timeseries,
        'stock': stock,
        'day': day,
        'candlestick': candlestick(),
    }

    return render(request, 'dashboard/index.html', context)
