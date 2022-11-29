# time series momentum，
# 函数将通过时间序列的对数回报、感兴趣的时间段以及是否允许做空的布尔变量来返回预期表现。
# -- coding: utf-8 --*
import ffn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import yfinance as yf  # 雅虎财经下载股票数据


import akshare as ak
# stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh000300', period='1')
# print(stock_zh_a_minute_df)

# %matplotlib inline

# 1-day return
def TSMstrategy(returns, period=1, shorts=False):
    if shorts:
        position = returns.rolling(period).mean().map(  # 移动平均线
            lambda x: -1 if x <= 0 else 1)
    else:
        position = returns.rolling(period).mean().map(
            lambda x: 0 if x <= 0 else 1)
    performance = position.shift(1) * returns
    return performance


ticker = 'TCS'  # 可以换成不同的ticker type，比如TCS/Infosys/Wipro
yftcs = yf.Ticker(ticker)
# data = yftcs.history(start='2005-01-01', end='2021-12-31')

data = yf.download(' '.join(Tickers), start=START_DATE, end=END_DATE,
                   group_by='ticker')

tickers_to_retry = []

for ticker in TICKERS:
    download_success = [r for r in data[ticker]['Close'] if r > 0]
    if download_success:
        CASHED_DATA[ticker] = {'close': [r for r in data[ticker]['Close']],
                               'row_data': data[ticker],
                               'low': [r for r in data[ticker]['Low']],
                               'high': [r for r in data[ticker]['High']]}
    else:
        tickers_to_retry.append(ticker)

if tickers_to_retry:
    data = yf.download(' '.join(tickers_to_retry), start=START_DATE, end=END_DATE,
                       group_by='ticker')

for ticker in tickers_to_retry:
    download_success = [r for r in data[ticker]['Close'] if r > 0]
    if download_success:
        CASHED_DATA[ticker] = {'close': [r for r in data[ticker]['Close']],
                               'row_data': data[ticker],
                               'low': [r for r in data[ticker]['Low']],
                               'high': [r for r in data[ticker]['High']]}

returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
performance = TSMstrategy(returns, period=1, shorts=False).dropna()
years = (performance.index.max() - performance.index.min()).days / 365
perf_cum = np.exp(performance.cumsum())
tot = perf_cum[-1] - 1
ann = perf_cum[-1] ** (1 / years) - 1
vol = performance.std() * np.sqrt(252)
rfr = 0.02
sharpe = (ann - rfr) / vol

print("1-day TSM strategy yields:" +
      "\n\t{tot * 100:.2f}% total returns" +
      "\n\t{ann * 100:.2f}% annual returns" +
      "\n\t{sharpe:.2f} Sharpe Ratio")

tcs_ret = np.exp(returns.cumsum())
b_tot = tcs_ret[-1] - 1
b_ann = tcs_ret[-1] ** (1 / years) - 1
b_vol = returns.std() * np.sqrt(252)
b_sharpe = (b_ann - rfr) / b_vol

print("Baseline Buy-and-Hold Strategy yields:" +
      "\n\t{b_tot * 100:.2f}% total returns" +
      "\n\t{b_ann * 100:.2f}% annual returns" +
      "\n\t{b_sharpe:.2f} Sharpe Ratio")

# what the output tells:


# 不同天数的时间段

periods = [3, 5, 15, 30, 90]
fig = plt.figure(figsize=(12, 10))

gs = fig.add_gridspec(4, 4)
ax0 = fig.add_subplot(gs[:2, :4])
ax1 = fig.add_subplot(gs[2:, :2])
ax2 = fig.add_subplot(gs[2:, 2:])
ax0.plot((np.exp(returns.cumsum()) - 1) * 100, label=ticker, linestyle='-')

perf_dict = {'tot_ret': {'buy_and_hold': (np.exp(returns.sum()) - 1)}, 'ann_ret': {'buy_and_hold': b_ann},
             'sharpe': {'buy_and_hold': b_sharpe}}

for p in periods:
    log_perf = TSMstrategy(returns, period=p, shorts=False)
    perf = np.exp(log_perf.cumsum())
    perf_dict['tot_ret']['p'] = (perf[-1] - 1)
    ann = (perf[-1] ** (1 / years) - 1)
    perf_dict['ann_ret']['p'] = ann
    vol = log_perf.std() * np.sqrt(252)
    perf_dict['sharpe']['p'] = (ann - rfr) / vol
    ax0.plot((perf - 1) * 100, label='{p}-Day Mean')

ax0.set_ylabel('Returns (%)')
ax0.set_xlabel('Date')
ax0.set_title('Cumulative Returns')
ax0.grid()
ax0.legend()

_ = [ax1.bar(i, v * 100) for i, v in enumerate(perf_dict['ann_ret'].values())]
ax1.set_xticks([i for i, k in enumerate(perf_dict['ann_ret'])])
ax1.set_xticklabels(['{k}-Day Mean'
                     if type(k) is int else ticker for
                     k in perf_dict['ann_ret'].keys()],
                    rotation=45)
ax1.grid()
ax1.set_ylabel('Returns (%)')
ax1.set_xlabel('Strategy')
ax1.set_title('Annual Returns')
_ = [ax2.bar(i, v) for i, v in enumerate(perf_dict['sharpe'].values())]
ax2.set_xticks([i for i, k in enumerate(perf_dict['sharpe'])])
ax2.set_xticklabels(['{k}-Day Mean'
                     if type(k) is int else ticker for
                     k in perf_dict['sharpe'].keys()],
                    rotation=45)
ax2.grid()
ax2.set_ylabel('Sharpe Ratio')
ax2.set_xlabel('Strategy')
ax2.set_title('Sharpe Ratio')
plt.tight_layout()
plt.show()

# 投资组合分析
import pandas_datareader as web
import time

stocks = ['SPY', 'GLD', 'TLT', 'HYG']
webData = pd.DataFrame()
for stock in stocks:
    webData[stock] = web.DataReader(stock, data_source='yahoo', start='', end='', retry_count=10)['Adj Close']
    # time.sleep(22)  # thread sleep for 22 seconds.
webData.sort_index(ascending=True, inplace=True)
perf = webData.calc_stats()
perf.plot()

# 对数回报
returns = webData.to_log_returns().dropna()
print(returns.head())
ax = returns.hist(figsize=(20, 10), bins=30)

# 最大回撤率
ffn.to_drawdown_series(data).plot(figsize=(15, 10))

# MARKOWITZ 均值-方差优化
returns.calc_mean_var_weights().as_format('.2%')

# 相关性统计
returns.plot_corr_heatmap()
