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
    

# compute ema and ema200
def get_EMA(df, n=7):
    # computes 200 EMA
    ema = df['close'].ewm(span=n, adjust=False).mean()
    ema_200 = df['close'].ewm(span=200, adjust=False).mean()
    
    df['EMA'] = ema
    df['EMA_200'] = ema_200
    
    return df

# implement buy/sell strategy
def implement_macd_bs_strategy(df):
    buy_list = []
    sell_list = []
    flag = -1
    
    for i in range(0,len(df)):
        # BUY Signal
        if (df['macd'][i] > df['signal'][i]):
            sell_list.append(np.nan)
            if (flag != 1) :
                flag = 1     
                if ( (df['high'][i] > df['EMA'][i]) and \
                    (df['macd'][i] < 0)   ):
                    buy_list.append(df['close'][i])
                else:
                    buy_list.append(np.nan) 
            else:
                buy_list.append(np.nan)
        
        # SELL Signal
        elif (df['macd'][i] < df['signal'][i]):
            
            buy_list.append(np.nan)
            if (flag != 0) :
                flag = 0
                if ( (df['low'][i] < df['EMA'][i]) and \
                    (df['macd'][i] > 0)   ) :
                    sell_list.append(df['close'][i])
                else:
                    sell_list.append(np.nan)    
            else:
                sell_list.append(np.nan)
        
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
            
    df['buy_signal'] = buy_list
    df['sell_signal'] = sell_list

    return df


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
            y=df['buy_signal'],
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
            y=df['sell_signal'],
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
    
    df_macd_ema = get_EMA(df_macd, 7)
    
    df_macd_bs = implement_macd_bs_strategy(df_macd_ema)

    plot_macd_with_bs(df_macd_bs)