# I0SDF9R4WZYH60B7


import yfinance as yf
import plotly.graph_objs as go
from alpha_vantage.timeseries import TimeSeries


def get_historical_data(currency,period='1d',interval='1m'):
    df = yf.download(currency,period=period,interval=interval)[['Close', 'Open', 'High', 'Low','Volume']]
    return df

# def get_historical_data(currency,period='1d',interval='1m'):
#     ts = TimeSeries(key='I0SDF9R4WZYH60B7',output_format='pandas', indexing_type='date')

#     df, meta_data =ts.get_intraday(symbol =currency,interval=interval)
#     return df


def update_fig(data,optmize_vision=True):
    fig = go.Figure()
    # Candlestick
    if optmize_vision:
        data = data.iloc[-100:,:]
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name = 'market data'))
    fig.update_layout(width=1600,height=600,autosize=True)
    return fig
