#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/28 12:22
# @Author  : Hao Wu
# @File    : .py
from classes.backtest.backtest import Backtest
backtest=Backtest()
paras = {
    'option_type': 'VanillaCall',
    'notional': 12e6,
    'start_date': '20190129',
    'end_date': '20191231',
    'K': 5.42,
    'stock_code': '300277.SZ',
    'start_price': 6.19
}
backtest.set_strategy('WW_Hedge')
backtest.set_option_portfolio(paras)
backtest.run_backtest(r=0.04, K=paras.get('K'), size=backtest.size)
backtest.plot_analysis()
