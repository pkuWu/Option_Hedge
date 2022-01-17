#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/7 12:00
# @Author  : Hao Wu
# @File    : .py
from classes.backtest.backtest import Backtest
from datetime import date
from classes.options.Vanilla import VanillaCall
from classes.options.OptionBase import OptionBase
from classes.strategy.WW_Hedge import WW_Hedge
from classes.strategy.Zakamouline import Zakamouline
# backtest = BacktestFramework()
vanilla = VanillaCall()
ww_hedge = WW_Hedge()
zakamouline = Zakamouline()
para_dict={'notional':12e6,
           'start_date':'20190129',
           'end_date':'20191230',
           'K':5.42,
           'option_fee':1780800,
           'stock_code':'300277.SZ',
           'start_price':6.19,
           'option_type':'call'}
# backtest.set_option(para_dict)
# option.stock_code
vanilla.set_paras_by_dict(para_dict)
vanilla.calculate_greeks()
vanilla.calculate_decomposition()

kwargs = {'r':0.04,
          'lambda':0.00005,
          'size':para_dict.get('notional')/para_dict.get('start_price'),
          'gamma':1,
          'K':5.42}
ww_hedge.get_hedging_position(vanilla.greek_df,**kwargs)
zakamouline.get_hedging_position(vanilla.greek_df,**kwargs)
ww_hedge.hedge_visualization(vanilla.greek_df)
zakamouline.hedge_visualization(vanilla.greek_df)

b = Backtest()
b.run_backtest(ww_hedge.df_hedge.loc[:, ['stock_price', 'position']])
b.summary()
