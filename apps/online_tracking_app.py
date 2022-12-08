# -*- coding: UTF-8 -*-
"""
@Project ：Forex_Analysis_Dash
@File ：online_tracking_app.py
@Author ： Bean
@Date ：11/24/22 1:50 PM
"""
from dash import html, dcc
from dash import callback, Input, State, Output
import feffery_antd_components as fac
from models.currency_config import CURRENCY_DICT, BEAR_BULL_COLOR, BEAR_BULL_ICON, AVAILABLE_INTERVAL
from models.utilities import map_dict_to_options
from models.online_query import get_historical_data,update_fig

"""
id definition
"""
id_ota_currency_sel = 'id_ota_currency_sel'
id_ota_submit_btn = 'id_ota_submit_btn'
id_ota_period_seg = 'id_ota_period_seg'
id_ota_current_open_price_stats = 'id_ota_current_open_price_stats'
id_ota_current_close_price_stats = 'id_ota_current_close_price_stats'
id_ota_refresh_interval = 'id_ota_refresh_interval'
id_ota_trend_fig = 'id_ota_trend_fig'
# initial values
init_currency = 'EURUSD=X'
init_interval = AVAILABLE_INTERVAL['M1']
init_df = get_historical_data(
    currency=init_currency, period=init_interval.period,interval=init_interval.interval)
init_open_price = init_df['Open'].values[-1]
init_close_price = init_df['Close'].values[-1]
init_fig = update_fig(init_df)




currency_sel = fac.AntdSelect(id=id_ota_currency_sel,
                              placeholder='select currency',
                              options=map_dict_to_options(CURRENCY_DICT),
                              value=init_currency,
                              style={
                                  'width': '400px'
                              }
                              )

submit_btn = fac.AntdButton(
    'Submit', id=id_ota_submit_btn, type='primary', danger=True)

period_seg = fac.AntdSegmented(id=id_ota_period_seg,
                               options=[
                                   {
                                       'label': k,
                                       'value': v.interval
                                   }
                                   for k, v in AVAILABLE_INTERVAL.items()
                               ],
                               defaultValue=init_interval.interval,
                               block=True
                               )

menu_row = fac.AntdRow(
    [
        fac.AntdCol(currency_sel,
                    span=6
                    ),
        fac.AntdCol(submit_btn,
                    span=4
                    ),
        fac.AntdCol(period_seg,
                    span=10,
                    offset=4
                    ),
    ], gutter=10
)

open_price_stats = fac.AntdStatistic(
    id=id_ota_current_open_price_stats,
    precision=2,
    title='Open Price',
    value=init_open_price,
    valueStyle={
        'color': BEAR_BULL_COLOR['bull']
    },
    prefix={
        'mode': 'icon',
        'content': BEAR_BULL_ICON['bull']
    }
)

close_price_stats = fac.AntdStatistic(
    id=id_ota_current_close_price_stats,
    precision=2,
    title='Close Price',
    value=init_close_price,
    valueStyle={
        'color': BEAR_BULL_COLOR['bull']
    },
    prefix={
        'mode': 'icon',
        'content': BEAR_BULL_ICON['bull']
    }
)

kpi_zone = fac.AntdCard(
    [open_price_stats,close_price_stats],
    title='Lastest Price',
    style={
        'width': '300px',
        'marginBottom': '10px'
    }
)

trend_fig = dcc.Graph(
        id=id_ota_trend_fig,figure=init_fig)


refresh_interval = dcc.Interval(
    id=id_ota_refresh_interval,
    n_intervals=0, interval=1000
)




# callback(
#     [Output('statistic-demo', 'value'),
#      Output('statistic-demo', 'prefix'),
#      Output('statistic-demo', 'valueStyle')],
#     Input('statistic-interval-demo', 'n_intervals'),
#     State('statistic-demo', 'value')
# )


# def statistic_demo_callback(n_intervals, value):
#     new_value = value + np.random.randn()

#     if new_value >= value:
#         return [
#             new_value,
#             {
#                 'mode': 'icon',
#                 'content': 'antd-rise'
#             },
#             {
#                 'color':}
#         ]

#     else:
#         return [
#             new_value,
#             {
#                 'mode': 'icon',
#                 'content': 'antd-fall'
#             },
#             {
#                 'color': '#3f8600'
#             }
#         ]


ota_layout = html.Div([html.H2('Online Tracking'), menu_row,
                       kpi_zone,trend_fig,
                       refresh_interval])
