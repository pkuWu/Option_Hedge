"""
@Author: Carl
@Time: 2022/1/22 9:18
@SoftWare: PyCharm
@File: main.py
"""
from classes.backtest.backtest import Backtest
from classes.options.Vanilla2 import VanillaCall, VanillaPut
from classes.options.option_portfolio2 import Strangle
from classes.strategy.ww_Hedge import WW_Hedge
from classes.strategy.zakamouline import Zakamouline

# set parameters
paras = {
    'option_type': 'Strangle',
    'notional': 12e6,
    'start_date': '20190129',
    'end_date': '20191231',
    'K': [5.42, 5.98],
    'stock_code': '300277.SZ',
    'start_price': 6.19
}

# test option
#%%
option = eval(paras.get('option_type'))()
option.set_paras_by_dict(para_dict=paras)
greek_df = option.get_greek_df()
option.decomposition_vis()

# test strategy
#%%
ww_hedge = WW_Hedge()
df_hedge_ww = ww_hedge.get_hedging_position(greek_df,
                              r=0.04,
                              size=12e6/6.19//100*100,
                              K=5.42)
ww_hedge.hedge_visualization(greek_df)

# test backtest
#%%
b = Backtest()
b.run_backtest(ww_hedge.df_hedge.loc[:, ['stock_price', 'position']])
b.summary()
