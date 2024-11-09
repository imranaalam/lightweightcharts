import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import json
import numpy as np
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Colors for candlestick and MACD charts
COLOR_BULL = 'rgba(38,166,154,0.9)'  # Green color for bullish
COLOR_BEAR = 'rgba(239,83,80,0.9)'   # Red color for bearish

st.set_page_config(page_title="Multipane Financial Chart", layout="wide")

# Fetch historical data for the AAPL stock using Yahoo Finance
@st.cache_data
def get_stock_data():
    ticker = yf.Ticker("AAPL")
    df = ticker.history(period='3mo', interval='1d')
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]

df = get_stock_data()

# Ensure we have enough data to calculate MACD
if df.empty or len(df) < 26:  # MACD needs at least 26 data points
    st.error("Not enough data to calculate MACD.")
    st.stop()

# Reset the index to turn the DateTimeIndex into a column
df.reset_index(inplace=True)

# Ensure the 'Date' column is of datetime type and convert to string format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date'], inplace=True)
df['time'] = df['Date'].dt.strftime('%Y-%m-%d')

# Add colors for bullish and bearish candlesticks
df['color'] = np.where(df['Open'] > df['Close'], COLOR_BEAR, COLOR_BULL)

# Calculate MACD using pandas_ta
try:
    macd_df = ta.macd(df['Close'], fast=6, slow=12, signal=5)
    if macd_df is None or macd_df.empty:
        raise ValueError("MACD calculation returned an empty DataFrame.")
    
    # Assign calculated columns to DataFrame
    df['MACD'] = macd_df['MACD_6_12_5']
    df['MACD_Signal'] = macd_df['MACDs_6_12_5']
    df['MACD_Hist'] = macd_df['MACDh_6_12_5']
except KeyError as e:
    st.error(f"Error calculating MACD: {e}")
    st.stop()
except Exception as e:
    st.error(f"Unexpected error calculating MACD: {e}")
    st.stop()

# Drop any rows with NaN values in the MACD columns
df.dropna(subset=['MACD', 'MACD_Signal', 'MACD_Hist'], inplace=True)

# Convert data to JSON format required by streamlit_lightweight_charts
try:
    candles = json.loads(df[['time', 'Open', 'High', 'Low', 'Close']].to_json(orient="records"))
    volume = json.loads(df[['time', 'Volume']].rename(columns={"Volume": "value"}).to_json(orient="records"))
except ValueError as e:
    st.error(f"Error converting DataFrame to JSON: {e}")
    st.stop()

# Convert the MACD, MACD Signal, and MACD Histogram to JSON format
macd_fast = json.loads(df[['time', 'MACD']].rename(columns={"MACD": "value"}).to_json(orient="records"))
macd_signal = json.loads(df[['time', 'MACD_Signal']].rename(columns={"MACD_Signal": "value"}).to_json(orient="records"))
macd_hist = json.loads(df[['time', 'MACD_Hist']].rename(columns={"MACD_Hist": "value"}).to_json(orient="records"))

# Generate colors for the MACD histogram
df['color'] = np.where(df['MACD_Hist'] > 0, COLOR_BULL, COLOR_BEAR)

# Chart configurations
chart_options = [
    {
        "width": 700,
        "height": 400,
        "layout": {"background": {"type": "solid", "color": "white"}, "textColor": "black"},
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"}
        },
        "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
        "timeScale": {"borderColor": "rgba(197, 203, 206, 0.8)", "barSpacing": 15}
    }
]

# Define the data series for the charts
series_candlestick = [
    {"type": 'Candlestick', "data": candles, 
     "options": {"upColor": COLOR_BULL, "downColor": COLOR_BEAR, "borderVisible": False, 
                 "wickUpColor": COLOR_BULL, "wickDownColor": COLOR_BEAR}}
]

series_volume = [
    {"type": 'Histogram', "data": volume, 
     "options": {"color": '#26a69a', "priceFormat": {"type": 'volume'}, "priceScaleId": ""}}
]

series_macd = [
    {"type": 'Line', "data": macd_fast, "options": {"color": 'blue', "lineWidth": 2}},
    {"type": 'Line', "data": macd_signal, "options": {"color": 'green', "lineWidth": 2}},
    {"type": 'Histogram', "data": macd_hist, "options": {"color": 'red', "lineWidth": 1}}
]

# Render the charts using renderLightweightCharts
st.subheader("Multipane Financial Chart - AAPL Stock")
renderLightweightCharts([
    {"chart": chart_options[0], "series": series_candlestick},
    {"chart": chart_options[0], "series": series_volume},
    {"chart": chart_options[0], "series": series_macd}
], 'multipane')
