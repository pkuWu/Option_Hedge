#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/7 12:00
# @Author  : Hao Wu
# @File    : .py
from classes.options.option_portfolio2 import OptionPortfolio
from classes.strategy.zakamouline import Zakamouline
from classes.strategy.ww_Hedge import WW_Hedge

# set parameters
paras = {
    'option_type': 'VanillaCall',
    'notional': 12e6,
    'start_date': '20190129',
    'end_date': '20191231',
    'K': 5.42,
    'stock_code': '300277.SZ',
    'start_price': 6.19
}

#%%
op = OptionPortfolio()
op.get_option_list(para_dict=paras)
greek_df = op.get_greek_df()
basic_paras_df = op.get_basic_paras_df()
size = op.get_size()

#%%
zk = Zakamouline()
zk.calculate_hedge_position(greek_df, basic_paras_df, r=0.04, K=5.42, size=size)
zk_hedge_df = zk.get_hedge_df()

#%%
ww = WW_Hedge()
ww.calculate_hedge_position(greek_df, basic_paras_df, r=0.04, K=5.42, size=size)
ww_hedge_df = ww.get_hedge_df()