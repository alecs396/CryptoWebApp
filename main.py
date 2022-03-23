from locale import currency
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time

# Title
st.title('Top 100 Crypto Price Change')

# Page Layout
col1 = st.sidebar
col2, col3 = st.columns((2,1))

# Sidebar + Main Panel config
col1.header('Input Options')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for proce', ('USD', 'USDT', 'BTC'))




