#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/21 23:19
# @Author  : Hao Wu
# @File    : .py

from classes.options.option_portfolio import Option_Portfolio

# test for Option_Portfolio
Spread_paras = {'portfolio_class': 'BullCallSpread',
             'notional':12e6,
             'start_date':'20190129',
             'end_date':'20191231',
             'K_low':5.42,
             'K_high':5.98,
             'stock_code':'300277.SZ',
             'start_price':6.19
             }

option_portfolio = Option_Portfolio()
option_portfolio.create_portfolio_dict(**Spread_paras)
option_portfolio.calculate_portfolio_greeks()
portfolio_greeks=option_portfolio.get_portfolio_df_greek()

# butterFly_paras = {'portfolio_class':'ButterflySpread',
#              'notional':12e6,
#              'start_date':'20190129',
#              'end_date':'20191231',
#              'K_low':5.42,
#              'K_high':5.98,
#              'stock_code':'300277.SZ',
#              'start_price':6.19,
#             }
#
# option_portfolio = Option_Portfolio()
# option_portfolio.create_portfolio_dict(**butterFly_paras)
# option_portfolio.calculate_portfolio_greeks()
# portfolio_greeks=option_portfolio.return_result()

# #%%
# strangle_paras = {'portfolio_class': 'Strangle',
#              'notional':12e6,
#              'start_date':'20190129',
#              'end_date':'20191231',
#              'K_low':5.42,
#              'K_high':5.98,
#              'stock_code':'300277.SZ',
#              'start_price':6.19
#             }
#
# option_portfolio = Option_Portfolio()
# option_portfolio.create_portfolio_dict(**strangle_paras)
# option_portfolio.calculate_portfolio_greeks()
# portfolio_greeks=option_portfolio.get_portfolio_df_greek()
#%%

