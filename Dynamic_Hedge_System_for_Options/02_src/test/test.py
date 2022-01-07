#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/12/28 21:58
# @Author  : Hao Wu
# @File    : .py
from classes.backtest.backtestFramework import BacktestFramework
from datetime import date
from classes.options.Vanilla import VanillaCall
from classes.options.OptionBase import OptionBase
backtest = BacktestFramework()
vanilla = VanillaCall()
option = OptionBase()
backtest.reset()
para_dict={'notional':12e6,
           'start_date':'20190129',
           'end_date':'20191230',
           'K':5.42,
           'option_fee':1780800,
           'stock_code':'300277.SZ',
           'start_price':6.02,
           'option_type':'call'}
backtest.set_option(para_dict)
option.stock_code
vanilla.calculate_greeks()
vanilla.greek_df
backtest.set_strategy('HedgeAll')
backtest.run_backtest()
