# -*- coding: UTF-8 -*-
"""
@Project ：Forex_Analysis_Dash
@File ：run.py
@Author ： Bean
@Date ：11/24/22 1:50 PM
"""
import dash
from apps.homepage_app import hp_layout

app = dash.Dash(__name__)
server = app.server
app.layout = hp_layout

if __name__ == '__main__':
    app.run_server(debug=True)
