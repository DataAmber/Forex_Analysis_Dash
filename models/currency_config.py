from dataclasses import dataclass

CURRENCY_DICT = {'EUR/USD': 'EURUSD=X',
                 'USD/JPY': 'JPY=X',
                 'GBP/USD': 'GBPUSD=X',
                 'USD/CNY': 'CNY=X'
                 }


BEAR_BULL_COLOR = {'bear': '#3f8600',
                   'bull': '#cf1322'}
BEAR_BULL_ICON = {'bear': '#antd-fall',
                  'bull': 'antd-rise'}

@dataclass
class QueryDt:
    period: str = '1d'
    interval: str = '1m'

AVAILABLE_INTERVAL = {'M1':QueryDt(period='1d',interval='1m'),
            'M5':QueryDt(period='1d',interval='5m'),
            'M30':QueryDt(period='5d',interval='30m'),
            'H1':QueryDt(period='5d',interval='1h'),
            'D1':QueryDt(period='3mo',interval='1d'),
            'W1':QueryDt(period='5y',interval='1wk'),
            'MN':QueryDt(period='max',interval='3mo')}