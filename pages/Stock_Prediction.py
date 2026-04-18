import streamlit as st
from pages.utils.model_train import *
import pandas as pd
from pages.utils.plotly_figure import *

st.set_page_config(
    page_title="Stock Prediction",
    layout='wide'
)

st.title("Stock Price Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

st.subheader('Predicting Next 30 days Close Price for: ' + ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

if isinstance(rolling_price.columns, pd.MultiIndex):
    rolling_price.columns = ['Close']
else:
    rolling_price.columns = ['Close']

rolling_price.index = pd.to_datetime(rolling_price.index)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)

rmse = evaluate_model(rolling_price, differencing_order)
st.write("**Model RMSE Score:**", rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast = forecast.copy()
forecast.columns = ['Close']

forecast.index = pd.to_datetime(forecast.index)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

st.write('### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

combined = pd.concat([rolling_price, forecast])
combined = combined.sort_index()

combined = combined.dropna()

plot_data = combined.iloc[-200:]


st.plotly_chart(
    Moving_average_forecast(plot_data),
    use_container_width=True
)

