# -*- coding: UTF-8 -*-
"""
@Project ：Forex_Analysis_Dash
@File ：homepage_app.py
@Author ： Bean
@Date ：11/24/22 1:50 PM
"""
from dash import callback, Input, Output, State
from apps.forecasting_app import fa_layout
from apps.backtest_app import bta_layout
from apps.online_tracking_app import ota_layout
from dash import html
import feffery_antd_components as fac

# ids
id_hp_title = 'id_hp_title'
id_hp_sidebar = 'id_hp_sidebar'
id_hp_content = 'id_hp_content'

# layout mapping
layout_mapping = {
    'online_tracking': ota_layout,
    'forecast': fa_layout,
    'backtest': bta_layout
}

# menu
title = fac.AntdTitle('Forex Analysis Dash', level=1, id=id_hp_title)

# sidebar
side_bar = html.Div(
    fac.AntdMenu(
        id=id_hp_sidebar,
        menuItems=[
            {
                'component': 'Item',
                'props': {
                    'key': f'online_tracking',
                    'title': f'Online Tracking',
                    'icon': 'antd-home'
                }},
            {
                'component': 'Item',
                'props': {
                    'key': f'forecast',
                    'title': f'Forecast',
                    'icon': 'antd-dot-chart'
                }},
            {
                'component': 'Item',
                'props': {
                    'key': f'backtest',
                    'title': f'Backtest',
                    'icon': 'antd-bar-chart'
                }}
        ],
        defaultSelectedKey='online_tracking',
        mode='inline',

    )
)

hp_layout = html.Div(
    [
        fac.AntdLayout(
            [
                fac.AntdHeader(
                    title,
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'alignItems': 'center',
                        'background': '#ffd700'
                    }
                ),
                fac.AntdLayout(
                    [
                        fac.AntdSider(side_bar, collapsible=True, style={'backgroundColor': '#ffffff'}),
                        fac.AntdLayout(
                            [
                                fac.AntdContent(
                                    id=id_hp_content,
                                    style={
                                        'display': 'flex',
                                        'height': '100%',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    }
                                ),
                                fac.AntdFooter(
                                    fac.AntdTitle(
                                        'Data Amber',
                                        level=3,
                                        style={
                                            'margin': '0',
                                            'float': 'right',
                                        }
                                    ), style={
                                        'justifyContent': 'end',
                                    }),
                            ]
                        )
                    ],
                )
            ]
            , style={
                'height': '960px'
            })
    ],
)


# callbacks
@callback(
    Output(id_hp_content, 'children'),
    [Input(id_hp_sidebar, 'currentKey')]
)
def menu_callback_demo(currentKey):
    return layout_mapping.get(currentKey)
