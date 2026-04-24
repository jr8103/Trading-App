import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import close_chart
from pages.utils.plotly_figure import RSI
from pages.utils.plotly_figure import Moving_average
from pages.utils.plotly_figure import MACD
from pages.utils.plotly_figure import candlestick

st.set_page_config(page_title="Stock Analysis", 
                   page_icon="bar_chart:", 
                   layout="wide")

st.title("Stock Analysis")

col1,col2,col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Enter Stock Ticker","AAPL")

with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year -1,today.month,today.day))

with col3:
    end_date = st.date_input("Choose End Date", today)

st.subheader(ticker)

stock=yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("**Sector:** ", stock.info['sector'])
st.write("**Employees:**",stock.info['fullTimeEmployees'])
st.write(stock.info['website'])

col1,col2=st.columns(2)

with col1:
    df = pd.DataFrame(index=['Market Cap','Beta','EPS','PE Ratio'])
    df[''] = [stock.info['marketCap'], stock.info['beta'], stock.info['trailingEps'], stock.info['trailingPE']]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df=pd.DataFrame(index=['Quick Ratio','Revenue per share','Profit Margins',
                           'Debt to Equity','Return on Equity'])
    df['']=[stock.info['quickRatio'], stock.info['revenuePerShare'], stock.info['profitMargins'],
           stock.info['debtToEquity'], stock.info['returnOnEquity']]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

data=yf.download(ticker,start=start_date,end=end_date)

col1,col2,col3 = st.columns(3)
if data is None or data.empty:
    st.error("No data found for this ticker or date range.")
else:
    # Fix multi-index issue (important for yfinance)
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

    if 'Close' not in data.columns:
        st.error("Close price not available.")
    elif len(data) < 2:
        st.error("Not enough data to calculate daily change.")
    else:
        latest = data['Close'].iloc[-1]
        previous = data['Close'].iloc[-2]

        if pd.isna(latest) or pd.isna(previous):
            st.error("Price data contains missing values.")
        else:
            latest = float(latest)
            previous = float(previous)

            daily_change = latest - previous
            percent = (daily_change / previous) * 100

            col1.metric(
                "Daily Change",
                f"{latest:.2f}",
                f"{daily_change:.2f} ({percent:.2f}%)"
            )
daily_change = latest - previous
percent = (daily_change / previous) * 100

col1.metric(
    "Daily Change",
    f"{latest:.2f}",
    f"{daily_change:.2f} ({percent:.2f}%)"
)

last_10_df = data.tail(10).sort_index(ascending=False).round(3)

# Fix column names
last_10_df.columns = [col[0] if isinstance(col, tuple) else col for col in last_10_df.columns]

fig_df = plotly_table(last_10_df)

st.write("##### Historical Data (Last 10 Days)")
st.plotly_chart(fig_df, use_container_width=True)

col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

num_period=''
with col1:
    if st.button('5D'):
        num_period='5d'
with col2:
    if st.button('1M'):
        num_period='1mo'
with col3:    
    if st.button('3M'):
        num_period='3mo'
with col4:
    if st.button('YTD'):
        num_period='ytd'
with col5:
    if st.button('1Y'):
        num_period='1y'
with col6:
    if st.button('5Y'):
        num_period='5y'
with col7:
    if st.button('MAX'):
        num_period='max'

col1,col2,col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox("", ("Line", "Candle"))
with col2:
    if chart_type =='Candle':

        indicators = st.selectbox('',('RSI','MACD'))
    else:
        indicators = st.selectbox('',('RSI','Moving Average','MACD'))

ticker_=yf.Ticker(ticker)
new_df1=ticker_.history(period='max')
data1 = ticker_.history(period = 'max')
if num_period=='':
    if chart_type == 'Candle' and indicators=='RSI':
        st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
        st.plotly_chart(RSI(data1,'1y'), use_container_width=True)

    if chart_type == 'Candle' and indicators=='MACD':
        st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
        st.plotly_chart(MACD(data1,'1y'), use_container_width=True)
    
    if chart_type == 'Line' and indicators=='RSI':
        st.plotly_chart(close_chart(data1,'1y'), use_container_width=True)
        st.plotly_chart(RSI(data1,'1y'), use_container_width=True)

    if chart_type == 'Line' and indicators=='Moving Average':
        st.plotly_chart(Moving_average(data1,'1y'), use_container_width=True)

    if chart_type == 'Line' and indicators=='MACD':
        st.plotly_chart(close_chart(data1,'1y'), use_container_width=True)
        st.plotly_chart(MACD(data1,'1y'), use_container_width=True)
else:
    if chart_type == 'Candle' and indicators=='RSI':
        st.plotly_chart(candlestick(data1,num_period), use_container_width=True)
        st.plotly_chart(RSI(data1,num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators=='MACD':
        st.plotly_chart(candlestick(data1,num_period), use_container_width=True)
        st.plotly_chart(MACD(data1,num_period), use_container_width=True)
    
    if chart_type == 'Line' and indicators=='RSI':
        st.plotly_chart(close_chart(data1,num_period), use_container_width=True)
        st.plotly_chart(RSI(data1,num_period), use_container_width=True)

    if chart_type == 'Line' and indicators=='Moving Average':
        st.plotly_chart(Moving_average(data1,num_period), use_container_width=True)

    if chart_type == 'Line' and indicators=='MACD':
        st.plotly_chart(close_chart(data1,num_period), use_container_width=True)
        st.plotly_chart(MACD(data1,num_period), use_container_width=True)
