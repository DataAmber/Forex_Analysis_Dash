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
from ta.trend import MACD

"""
compute_macd：根据收盘价计算MACD
plot_macd：图中画出MACD line和Signal line
implement_macd_strategy：根据MACD和Signal实现买入卖出策略
plot_macd_with_bs：图中标记买入卖出信号
"""
def compute_macd(df, slow, fast, smooth):
    macd_trend = MACD(df['close'], window_slow=slow, window_fast=fast, window_sign=smooth)
    df['macd'] = macd_trend.macd()
    df['signal'] = macd_trend.macd_signal()
    df['hist'] = macd_trend.macd_diff()
    return df


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
                color=['rgba(63, 195, 128, 1)' if v > 0 else 'rgba(219, 10, 91, 1)' for v in df['hist']]
            )
        ),
        row=2, col=1
    )
    fig.update_layout(height=600, width=800, title_text="MACD and Signal Line")
    fig.show()


def implement_macd_strategy(data):
    data['buy_price'] = data['close']
    data['sell_price'] = data['close']
    data['signal_sign'] = (data['macd'] > data['signal']).replace({True: 1, False: 0})
    data['signal_sign_diff'] = data['signal_sign'].diff().fillna(0)
    data.loc[data['signal_sign_diff'] != 1, 'buy_price'] = np.nan
    data.loc[data['signal_sign_diff'] != -1, 'sell_price'] = np.nan
    return data


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
                color='green',
                symbol='triangle-up',
                size=8,
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
                color='red',
                symbol='triangle-down',
                size=8,
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
                color=['rgba(63, 195, 128, 1)' if v > 0 else 'rgba(219, 10, 91, 1)' for v in df['hist']]
            )
        ),
        row=2, col=1
    )

    fig.update_layout(height=600, width=800, title_text="MACD and Signal Line")
    fig.show()


if "__main__" == __name__:
    data_path = r'../data/BTC_USD.csv'
    df = pd.read_csv(data_path)
    df = df.dropna(axis=0, how='any')
    df = df.reset_index(drop=True)
    df_macd = compute_macd(df, 26, 12, 9)
    df_macd = implement_macd_strategy(df_macd)
    plot_macd_with_bs(df_macd)
