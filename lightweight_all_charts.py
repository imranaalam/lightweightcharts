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

# Set page configuration
st.set_page_config(page_title="Lightweight Charts Dashboard", layout="wide")

# Sidebar for chart selection
st.sidebar.title("Select a Chart")
chart_options = [
    "Price and Volume Series Chart",
    "Overlaid Series with Markers",
    "Multipane Chart with Pandas",
    "Multipane Chart (Intraday) from CSV",
    "Line Chart",
    "Area Chart",
    "Histogram Chart",
    "Bar Chart",
    "Candlestick Chart",
    "Baseline Chart"
]
selected_chart = st.sidebar.selectbox("Choose a chart to display:", chart_options)

# Function Definitions for Each Chart

def price_and_volume_series_chart():
    import streamlit_lightweight_charts.dataSamples as data

    priceVolumeChartOptions = {
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.2,
                "bottom": 0.25,
            },
            "borderVisible": False,
        },
        "overlayPriceScales": {
            "scaleMargins": {
                "top": 0.7,
                "bottom": 0,
            }
        },
        "layout": {
            "background": {
                "type": 'solid',
                "color": '#131722'
            },
            "textColor": '#d1d4dc',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.6)',
            }
        }
    }

    priceVolumeSeries = [
        {
            "type": 'Area',
            "data": data.priceVolumeSeriesArea,
            "options": {
                "topColor": 'rgba(38,198,218, 0.56)',
                "bottomColor": 'rgba(38,198,218, 0.04)',
                "lineColor": 'rgba(38,198,218, 1)',
                "lineWidth": 2,
            }
        },
        {
            "type": 'Histogram',
            "data": data.priceVolumeSeriesHistogram,
            "options": {
                "color": '#26a69a',
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": ""  # Overlay setting
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0.7,
                    "bottom": 0,
                }
            }
        }
    ]
    st.subheader("Price and Volume Series Chart")
    renderLightweightCharts([
        {
            "chart": priceVolumeChartOptions,
            "series": priceVolumeSeries
        }
    ], 'priceAndVolume')

def overlaid_series_with_markers():
    import streamlit_lightweight_charts.dataSamples as data

    overlaidAreaSeriesOptions = {
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.1,
                "bottom": 0.1,
            },
            "mode": 2,  # PriceScaleMode: 0-Normal, 1-Logarithmic, 2-Percentage, 3-IndexedTo100
            "borderColor": 'rgba(197, 203, 206, 0.4)',
        },
        "timeScale": {
            "borderColor": 'rgba(197, 203, 206, 0.4)',
        },
        "layout": {
            "background": {
                "type": 'solid',
                "color": '#100841'
            },
            "textColor": '#ffffff',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(197, 203, 206, 0.4)',
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            },
            "horzLines": {
                "color": 'rgba(197, 203, 206, 0.4)',
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            }
        }
    }

    seriesOverlaidChart = [
        {
            "type": 'Area',
            "data": data.seriesMultipleChartArea01,
            "options": {
                "topColor": 'rgba(255, 192, 0, 0.7)',
                "bottomColor": 'rgba(255, 192, 0, 0.3)',
                "lineColor": 'rgba(255, 192, 0, 1)',
                "lineWidth": 2,
            },
            "markers": [
                {
                    "time": '2019-04-08',
                    "position": 'aboveBar',
                    "color": 'rgba(255, 192, 0, 1)',
                    "shape": 'arrowDown',
                    "text": 'H',
                    "size": 3
                },
                {
                    "time": '2019-05-13',
                    "position": 'belowBar',
                    "color": 'rgba(255, 192, 0, 1)',
                    "shape": 'arrowUp',
                    "text": 'L',
                    "size": 3
                },
            ]
        },
        {
            "type": 'Area',
            "data": data.seriesMultipleChartArea02,
            "options": {
                "topColor": 'rgba(67, 83, 254, 0.7)',
                "bottomColor": 'rgba(67, 83, 254, 0.3)',
                "lineColor": 'rgba(67, 83, 254, 1)',
                "lineWidth": 2,
            },
            "markers": [
                {
                    "time": '2019-05-03',
                    "position": 'aboveBar',
                    "color": 'rgba(67, 83, 254, 1)',
                    "shape": 'arrowDown',
                    "text": 'PEAK',
                    "size": 3
                },
            ]
        }
    ]
    st.subheader("Overlaid Series with Markers")
    renderLightweightCharts([
        {
            "chart": overlaidAreaSeriesOptions,
            "series": seriesOverlaidChart
        }
    ], 'overlaid')

def multipane_chart_with_pandas():
    # Define colors
    COLOR_BULL = 'rgba(38,166,154,0.9)'  # Green color for bullish candles
    COLOR_BEAR = 'rgba(239,83,80,0.9)'   # Red color for bearish candles

    # Fetch historical data using Yahoo Finance
    @st.cache_data
    def fetch_stock_data():
        ticker = yf.Ticker("AAPL")
        data = ticker.history(period='6mo', interval='1d')  # Increased period to 6 months for more data
        return data[['Open', 'High', 'Low', 'Close', 'Volume']]

    # Load the data
    df = fetch_stock_data()

    # Check if data is available and sufficient
    if df.empty or len(df) < 26:
        st.error("Not enough data available to generate the chart.")
        return

    # Data Preprocessing: Reset index and convert Date column to datetime
    df.reset_index(inplace=True)

    # Convert 'Date' to datetime, handling any parsing errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)  # Drop rows where date conversion failed

    # Format 'time' column to string format for charting
    df['time'] = df['Date'].dt.strftime('%Y-%m-%d')

    # Add colors for bullish and bearish candlesticks
    df['color'] = np.where(df['Open'] > df['Close'], COLOR_BEAR, COLOR_BULL)

    # Calculate MACD using pandas_ta
    try:
        macd = ta.macd(df['Close'], fast=6, slow=12, signal=5)
        if macd is None or macd.empty:
            raise ValueError("MACD calculation returned an empty DataFrame.")
        
        # Assign MACD values to the DataFrame
        df['MACD'] = macd['MACD_6_12_5']
        df['MACD_Signal'] = macd['MACDs_6_12_5']
        df['MACD_Hist'] = macd['MACDh_6_12_5']
    except Exception as e:
        st.error(f"Error calculating MACD: {e}")
        return

    # Drop rows with NaN values in the MACD columns
    df.dropna(subset=['MACD', 'MACD_Signal', 'MACD_Hist'], inplace=True)

    # Convert DataFrame to JSON format for the charts
    try:
        candles = json.loads(df[['time', 'Open', 'High', 'Low', 'Close']].to_json(orient='records'))
        volume = json.loads(df[['time', 'Volume']].rename(columns={'Volume': 'value'}).to_json(orient='records'))
    except ValueError as e:
        st.error(f"Error converting DataFrame to JSON: {e}")
        return

    try:
        macd_fast = json.loads(df[['time', 'MACD']].rename(columns={'MACD': 'value'}).to_json(orient='records'))
        macd_signal = json.loads(df[['time', 'MACD_Signal']].rename(columns={'MACD_Signal': 'value'}).to_json(orient='records'))
        macd_hist = json.loads(df[['time', 'MACD_Hist']].rename(columns={'MACD_Hist': 'value'}).to_json(orient='records'))
    except ValueError as e:
        st.error(f"Error converting MACD data to JSON: {e}")
        return

    # Chart configuration
    chart_options = {
        "width": 800,
        "height": 400,
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black"
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"}
        },
        "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
        "timeScale": {"borderColor": "rgba(197, 203, 206, 0.8)", "barSpacing": 15}
    }

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
        {"chart": chart_options, "series": series_candlestick},
        {"chart": chart_options, "series": series_volume},
        {"chart": chart_options, "series": series_macd}
    ], 'multipane')

def multipane_chart_intraday_from_csv():
    COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
    COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

    CSVFILE = 'https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/MultiPaneChartsFromCSV.csv?raw=true'

    try:
        df = pd.read_csv(CSVFILE, skiprows=0, parse_dates=['datetime'], skip_blank_lines=True)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return

    # Check if data is sufficient
    if df.empty or len(df) < 26:
        st.error("Not enough data in CSV to generate the chart.")
        return

    # Convert 'datetime' to UNIX timestamp
    try:
        df['time'] = df['datetime'].view('int64') // 10**9  # UNIX timestamp
    except Exception as e:
        st.error(f"Error converting datetime to UNIX timestamp: {e}")
        return

    df['color'] = np.where(df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear

    # Export to JSON format
    try:
        candles = json.loads(
            df.filter(['time', 'open', 'high', 'low', 'close'], axis=1)
              .to_json(orient="records")
        )

        volume = json.loads(
            df.filter(['time', 'volume'], axis=1)
              .rename(columns={"volume": "value"})
              .to_json(orient="records")
        )

        macd_fast = json.loads(
            df.filter(['time', 'macd_fast'], axis=1)
              .rename(columns={"macd_fast": "value"})
              .to_json(orient="records")
        )

        macd_slow = json.loads(
            df.filter(['time', 'macd_slow'], axis=1)
              .rename(columns={"macd_slow": "value"})
              .to_json(orient="records")
        )

        df['color'] = np.where(df['macd_hist'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
        macd_hist = json.loads(
            df.filter(['time', 'macd_hist'], axis=1)
              .rename(columns={"macd_hist": "value"})
              .to_json(orient="records")
        )
    except ValueError as e:
        st.error(f"Error converting DataFrame to JSON: {e}")
        return

    # Chart configuration
    chartMultipaneOptions = {
        "width": 800,
        "height": 400,
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black"
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"}
        },
        "crosshair": {
            "mode": 0
        },
        "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 10,
            "minBarSpacing": 8,
            "timeVisible": True,
            "secondsVisible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 48,
            "horzAlign": 'center',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.3)',
            "text": 'Intraday',
        }
    }

    seriesCandlestickChart = [
        {
            "type": 'Candlestick',
            "data": candles,
            "options": {
                "upColor": COLOR_BULL,
                "downColor": COLOR_BEAR,
                "borderVisible": False,
                "wickUpColor": COLOR_BULL,
                "wickDownColor": COLOR_BEAR
            }
        }
    ]

    seriesVolumeChart = [
        {
            "type": 'Histogram',
            "data": volume,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                "color": '#26a69a',
                "priceScaleId": ""  # Overlay setting
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0,
                    "bottom": 0,
                },
                "alignLabels": False
            }
        }
    ]

    seriesMACDchart = [
        {
            "type": 'Line',
            "data": macd_fast,
            "options": {
                "color": 'blue',
                "lineWidth": 2
            }
        },
        {
            "type": 'Line',
            "data": macd_slow,
            "options": {
                "color": 'green',
                "lineWidth": 2
            }
        },
        {
            "type": 'Histogram',
            "data": macd_hist,
            "options": {
                "color": 'red',
                "lineWidth": 1
            }
        }
    ]

    # Render the charts using renderLightweightCharts
    st.subheader("Multipane Chart (Intraday) from CSV")
    renderLightweightCharts([
        {"chart": chartMultipaneOptions, "series": seriesCandlestickChart},
        {"chart": chartMultipaneOptions, "series": seriesVolumeChart},
        {"chart": chartMultipaneOptions, "series": seriesMACDchart}
    ], 'multipane_csv')

def line_chart():
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesLineChart = [{
        "type": 'Line',
        "data": [
            { "time": '2018-12-22', "value": 32.51 },
            { "time": '2018-12-23', "value": 31.11 },
            { "time": '2018-12-24', "value": 27.02 },
            { "time": '2018-12-25', "value": 27.32 },
            { "time": '2018-12-26', "value": 25.17 },
            { "time": '2018-12-27', "value": 28.89 },
            { "time": '2018-12-28', "value": 25.46 },
            { "time": '2018-12-29', "value": 23.92 },
            { "time": '2018-12-30', "value": 22.68 },
            { "time": '2018-12-31', "value": 22.67 },
        ],
        "options": {}
    }]

    st.subheader("Line Chart with Watermark")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line')

def area_chart():
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesAreaChart = [{
        "type": 'Area',
        "data": [
            { "time": '2018-12-22', "value": 32.51 },
            { "time": '2018-12-23', "value": 31.11 },
            { "time": '2018-12-24', "value": 27.02 },
            { "time": '2018-12-25', "value": 27.32 },
            { "time": '2018-12-26', "value": 25.17 },
            { "time": '2018-12-27', "value": 28.89 },
            { "time": '2018-12-28', "value": 25.46 },
            { "time": '2018-12-29', "value": 23.92 },
            { "time": '2018-12-30', "value": 22.68 },
            { "time": '2018-12-31', "value": 22.67 },
        ],
        "options": {}
    }]

    st.subheader("Area Chart with Watermark")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesAreaChart,
        }
    ], 'area')

def histogram_chart():
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesHistogramChart = [{
        "type": 'Histogram',
        "data": [
            { "value": 1, "time": 1642425322 },
            { "value": 8, "time": 1642511722 },
            { "value": 10, "time": 1642598122 },
            { "value": 20, "time": 1642684522 },
            { "value": 3, "time": 1642770922, "color": 'red' },
            { "value": 43, "time": 1642857322 },
            { "value": 41, "time": 1642943722, "color": 'red' },
            { "value": 43, "time": 1643030122 },
            { "value": 56, "time": 1643116522 },
            { "value": 46, "time": 1643202922, "color": 'red' }
        ],
        "options": { "color": '#26a69a' }
    }]

    st.subheader("Histogram Chart with Watermark")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesHistogramChart
        }
    ], 'histogram')

def bar_chart():
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesBarChart = [{
        "type": 'Bar',
        "data": [
            { "open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "time": 1642427876 },
            { "open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "time": 1642514276 },
            { "open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "time": 1642600676 },
            { "open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "time": 1642687076 },
            { "open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "time": 1642773476 },
            { "open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "time": 1642859876 },
            { "open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "time": 1642946276 },
            { "open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "time": 1643032676 },
            { "open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "time": 1643119076 },
            { "open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "time": 1643205476 }
        ],
        "options": {
            "upColor": '#26a69a',
            "downColor": '#ef5350'
        }
    }]

    st.subheader("Bar Chart with Watermark")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesBarChart
        }
    ], 'bar')

def candlestick_chart():
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesCandlestickChart = [{
        "type": 'Candlestick',
        "data": [
            { "open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "time": 1642427876 },
            { "open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "time": 1642514276 },
            { "open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "time": 1642600676 },
            { "open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "time": 1642687076 },
            { "open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "time": 1642773476 },
            { "open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "time": 1642859876 },
            { "open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "time": 1642946276 },
            { "open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "time": 1643032676 },
            { "open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "time": 1643119076 },
            { "open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "time": 1643205476 }
        ],
        "options": {
            "upColor": '#26a69a',
            "downColor": '#ef5350',
            "borderVisible": False,
            "wickUpColor": '#26a69a',
            "wickDownColor": '#ef5350'
        }
    }]

    st.subheader("Candlestick Chart with Watermark")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesCandlestickChart
        }
    ], 'candlestick')

def baseline_chart():
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesBaselineChart = [{
        "type": 'Baseline',
        "data": [
            { "value": 1, "time": 1642425322 },
            { "value": 8, "time": 1642511722 },
            { "value": 10, "time": 1642598122 },
            { "value": 20, "time": 1642684522 },
            { "value": 3, "time": 1642770922 },
            { "value": 43, "time": 1642857322 },
            { "value": 41, "time": 1642943722 },
            { "value": 43, "time": 1643030122 },
            { "value": 56, "time": 1643116522 },
            { "value": 46, "time": 1643202922 }
        ],
        "options": {
            "baseValue": { "type": "price", "price": 25 },
            "topLineColor": 'rgba(38, 166, 154, 1)',
            "topFillColor1": 'rgba(38, 166, 154, 0.28)',
            "topFillColor2": 'rgba(38, 166, 154, 0.05)',
            "bottomLineColor": 'rgba(239, 83, 80, 1)',
            "bottomFillColor1": 'rgba(239, 83, 80, 0.05)',
            "bottomFillColor2": 'rgba(239, 83, 80, 0.28)'
        }
    }]

    st.subheader("Baseline Chart with Watermark")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesBaselineChart
        }
    ], 'baseline')

# Mapping chart options to functions
chart_functions = {
    "Price and Volume Series Chart": price_and_volume_series_chart,
    "Overlaid Series with Markers": overlaid_series_with_markers,
    "Multipane Chart with Pandas": multipane_chart_with_pandas,
    "Multipane Chart (Intraday) from CSV": multipane_chart_intraday_from_csv,
    "Line Chart": line_chart,
    "Area Chart": area_chart,
    "Histogram Chart": histogram_chart,
    "Bar Chart": bar_chart,
    "Candlestick Chart": candlestick_chart,
    "Baseline Chart": baseline_chart
}

# Display the selected chart
if selected_chart in chart_functions:
    chart_functions[selected_chart]()
else:
    st.write("Please select a chart from the sidebar.")

# Optional: Add an About section
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info("""
This Streamlit application showcases various financial charts using the [Lightweight Charts](https://github.com/tradingview/lightweight-charts) library wrapped by the [streamlit-lightweight-charts](https://github.com/freyastreamlit/streamlit-lightweight-charts) package.

**Features**:
- Interactive and performant financial charts
- Multiple chart types: Line, Area, Histogram, Bar, Candlestick, Baseline, and more
- Data sourced from Yahoo Finance and CSV files
- Customizable layouts and styles

**Developed by**: [Freyastreamlit](https://github.com/freyastreamlit)
""")
