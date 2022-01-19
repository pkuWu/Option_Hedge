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

# test for Vanilla
vanilla.set_paras(notional=12e6,
                  start_date='20190129',
                  end_date='20191231',
                  K=5.42,
                  option_fee=1780800,
                  stock_code='300277.SZ',
                  start_price=6.19)
vanilla.calculate_greeks()
vanilla.calculate_decomposition()
greek_df = vanilla.return_result()

# test for strategy
df_hedge_ww = ww_hedge.get_hedging_position(greek_df,
                              r=0.04,
                              Lambda=0.00005,
                              size=12e6/6.19//100*100,
                              gamma=0.5,
                              K=5.42)
df_hedge_zaka = zakamouline.get_hedging_position(greek_df,
                              r=0.04,
                              Lambda=0.00005,
                              size=12e6/6.19//100*100,
                              gamma=0.5,
                              K=5.42)
ww_hedge.hedge_visualization(greek_df)
zakamouline.hedge_visualization(greek_df)

b = Backtest()
b.run_backtest(ww_hedge.df_hedge.loc[:, ['stock_price', 'position']])
b.summary()
