import streamlit as st
import pandas as pd
import altair as alt
from pandas_datareader import data as web
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime
import time
import random


st.title("The Results from Trading Using Investiva")
st.write("Here, we share with you some of the results from our trading agent, Investiva.")

asset = 'MSFT'
 
# Getting the OHLCV data through API.
df = web.DataReader(asset, data_source='yahoo', start='01-01-2020')

###############################################################################

# Choosing what data to include in the plot
trace1 = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': asset,
    'showlegend': True
}

data = [trace1]

# Config graph layout
layout = go.Layout({
    'title': {
        'text': '<b>Microsoft Chart<b>',
        'font': {
            'size': 20
        }
    }
})

chart = go.Figure(data=data, layout=layout)

# Adding a check box to enable seeing the chart, if required.
if st.checkbox('Show Live Chart'):
    st.plotly_chart(chart)

# Adding a check box to enable seeing the numerical data, if required.
if st.checkbox('Show Numerical Data'):
    st.write(df.tail())


###############################################################################

# Initiate Yahoo Finance for a specific asset
stock = yf.Ticker(asset)

# Get stock info.
info = stock.info

# Filter the data to keep only the values we need.
to_keep = ['symbol', 'longName', 'market', 'sector', 'marketCap', 'open', 'previousClose','ask', 'bid', 
            'volume', 'averageVolume', 'averageDailyVolume10Day', 'shortRatio', 'earningsQuarterlyGrowth']
filtered_data = {x: info[x] for x in to_keep}
filterd_data_df = pd.DataFrame.from_dict(filtered_data, orient= 'index', columns=["value"])

if st.checkbox("Show Asset's Information"):
    st.write(filterd_data_df)
    # st.dataframe(filterd_data_df)

###############################################################################

# Some test text.
if st.checkbox("Show Live Trades"):
    trades = pd.DataFrame()
    my_table = st.empty()
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        output = [f"A Buy order for 1000 {asset} stocks has been placed. Buy price is $108.04",
                  f"A Sell order for 1000 {asset} stocks has been placed. Buy price is $109.25",
                  f"A Buy order for 750 {asset} stocks has been placed. Buy price is $107.20",
                  f"A Sell order for 750 {asset} stocks has been placed. Buy price is $111.41"]

        trades_dict={"Time Stamp": current_time, "Order":random.choice(output)}
        trades_df = pd.DataFrame.from_dict(trades_dict, orient= 'index', columns=["Orders"])
        # trades_df = pd.DataFrame(trades_dict.items(), columns=['Time', 'Order'])
        trades = trades.append(trades_df)
        # st.write(trades)
        my_table.dataframe(trades)
        time.sleep(5)









# # Calculate and define moving average of 30 periods
# avg_30 = df.Close.rolling(window=30, min_periods=1).mean()

# # Calculate and define moving average of 50 periods
# avg_50 = df.Close.rolling(window=50, min_periods=1).mean()

# trace2 = {
#     'x': df.index,
#     'y': avg_30,
#     'type': 'scatter',
#     'mode': 'lines',
#     'line': {
#         'width': 1,
#         'color': 'blue'
#             },
#     'name': 'Moving Average of 30 periods'
# }

# trace3 = {
#     'x': df.index,
#     'y': avg_50,
#     'type': 'scatter',
#     'mode': 'lines',
#     'line': {
#         'width': 1,
#         'color': 'red'
#     },
#     'name': 'Moving Average of 50 periods'
# }