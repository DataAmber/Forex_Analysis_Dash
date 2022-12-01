# -*- coding: UTF-8 -*-
"""
@Project ：Forex_Analysis_Dash
@File ：MACD.py
@Author ： Robin
@Date ：12/01/22 10:40 PM
"""
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


"""
compute_macd：根据收盘价计算MACD
plot_macd：图中画出MACD line和Signal line
implement_macd_strategy：根据MACD和Signal实现买入卖出策略
plot_macd_with_bs：图中标记买入卖出信号
"""
def compute_macd(df, slow, fast, smooth):
    price = df["close"]
    exp1 = price.ewm(span = fast, adjust = False).mean() # fast ema
    exp2 = price.ewm(span = slow, adjust = False).mean() # slow ema
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'}) # signal line
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [df, macd, signal, hist]
    df_res = pd.concat(frames, join = 'inner', axis = 1)
    return df_res

def plot_macd(df):
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Scatter(
            name='收盘价', 
            x=df['Date'], 
            y=df['close']
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            name='MACD Line', 
            x=df['Date'], 
            y=df['macd'],
            marker=dict(
                color='red'
            )
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            name='Signal Line', 
            x=df['Date'], 
            y=df['signal'],
            marker=dict(
                color='green'
            )
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(
            name='hist', 
            x=df['Date'], 
            y=df['hist'],
            marker=dict(
                color = ['rgba(63, 195, 128, 1)' if v >0 else 'rgba(219, 10, 91, 1)' for v in df['hist']]
            )
        ),
        row=2, col=1
    )

    fig.update_layout(height=600, width=800, title_text="MACD and Signal Line")
    fig.show()
    
    
def implement_macd_strategy(prices, data):    
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['macd'][i] > data['signal'][i]:  # 买入信号
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]: # 卖出信号
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
            
    return buy_price, sell_price, macd_signal


def plot_macd_with_bs(df):
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Scatter(
            name='收盘价', 
            x=df['Date'], 
            y=df['close']
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            name='buy signal', 
            x=df['Date'], 
            y=df['buy_price'],
            mode="lines+markers",
            marker=dict(
                color = 'green',
                symbol = 'triangle-up',
                size = 8,
            )
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            name='sell signal', 
            x=df['Date'], 
            y=df['sell_price'],
            mode="lines+markers",
            marker=dict(
                color = 'red',
                symbol = 'triangle-down',
                size = 8,
            )
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            name='MACD Line', 
            x=df['Date'], 
            y=df['macd'],
            marker=dict(
                color='red'
            )
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            name='Signal Line', 
            x=df['Date'], 
            y=df['signal'],
            marker=dict(
                color='green'
            )
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(
            name='hist', 
            x=df['Date'], 
            y=df['hist'],
            marker=dict(
                color = ['rgba(63, 195, 128, 1)' if v >0 else 'rgba(219, 10, 91, 1)' for v in df['hist']]
            )
        ),
        row=2, col=1
    )

    fig.update_layout(height=600, width=800, title_text="MACD and Signal Line")
    fig.show()

if "__main__"==__name__:
    data_path = r'algrithms\data\BTC_USD.csv'
    df = pd.read_csv(data_path)
    
    df = df.dropna(axis=0, how='any')
    df = df.reset_index(drop=True)
    
    df_macd = compute_macd(df, 26, 12, 9)
    
    buy_price, sell_price, macd_signal = implement_macd_strategy(df_macd['close'], df_macd)
    df_macd['buy_price'] = buy_price
    df_macd['sell_price'] = sell_price
    df_macd['macd_signal'] = macd_signal

    plot_macd_with_bs(df_macd)