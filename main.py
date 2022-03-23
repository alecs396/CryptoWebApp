from locale import currency
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import keys

# Title
st.title('Top 100 Crypto Price Change')

# Page Layout
col1 = st.sidebar
col2, col3 = st.columns((2,1))

# Sidebar + Main Panel config
col1.header('Input Options')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'USDT', 'BTC'))

# Gather data by scraping from CoinMarketCap
@st.cache
def load_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': keys.KEY,
    }

    session = Session()
    session.headers.update(headers)

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
  
        for i in data['data']:
            coin_name.append(i['slug'])
            coin_symbol.append(i['symbol'])
            price.append(i['quote'][currency_price_unit]['price'])
            percent_change_1h.append(i['quote'][currency_price_unit]['percent_change_1h'])
            percent_change_24h.append(i['quote'][currency_price_unit]['percent_change_24h'])
            percent_change_7d.append(i['quote'][currency_price_unit]['percent_change_7d'])
            market_cap.append(i['quote'][currency_price_unit]['market_cap'])
            volume_24h.append(i['quote'][currency_price_unit]['volume_24h'])
        
        df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
        df['coin_name'] = coin_name
        df['coin_symbol'] = coin_symbol
        df['price'] = price
        df['percent_change_1h'] = percent_change_1h
        df['percent_change_24h'] = percent_change_24h
        df['percent_change_7d'] = percent_change_7d
        df['market_cap'] = market_cap
        df['volume_24h'] = volume_24h
      
        return df
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    

df = load_data()

## Sidebar - Crypto Selections
sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]

## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]