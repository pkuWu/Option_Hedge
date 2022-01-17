#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/7 17:07
# @Author  : Hao Wu
# @File    : .py
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/12/29 21:46
# @Author  : Hao Wu
# @File    :
import pandas as pd
import numpy as np
from .strategyBase import StrategyBase


class WW_Hedge(StrategyBase):
    def __init__(self):
        super(WW_Hedge, self).__init__()

    def get_hedging_position(self,greek_df,**kwargs):
        # kwargs= {'r':r,'lambda':lambda,'size':size,'gamma':gamma}
        # size = notional/start_price
        greek_df = greek_df.reset_index()
        self.df_hedge = pd.DataFrame(columns=['stock_price', 'H0','delta','up_bound','low_bound'])
        self.df_hedge.loc[:, 'stock_price'] = greek_df.loc[:, 'stock_price']
        self.df_hedge.loc[:, 'H0'] = (3/2*np.exp(-kwargs['r']*greek_df.loc[:, 'left_times'])*kwargs['lambda']*greek_df.loc[:,'stock_price']*greek_df.loc[:,'gamma']**2/kwargs['gamma'])**(1/3)
        self.df_hedge.loc[:, 'delta'] = greek_df.loc[:, 'delta']
        self.df_hedge.loc[:, 'up_bound'] = self.df_hedge.loc[:, 'delta'] + self.df_hedge.loc[:, 'H0']
        self.df_hedge.loc[:, 'low_bound'] = self.df_hedge.loc[:, 'delta'] - self.df_hedge.loc[:, 'H0']
        position = 0
        position_rate = self.df_hedge.loc[:, 'delta'][0]
        for i in range(0, self.df_hedge.shape[0]):
            if position_rate < self.df_hedge.loc[i, 'low_bound'] or position_rate>self.df_hedge.loc[i,'up_bound']:
                position = self.df_hedge.loc[i, 'delta']*kwargs['size']//100*100
                position_rate = position/kwargs['size']
            self.df_hedge.loc[i, 'position'] = position
            self.df_hedge.loc[i, 'position_rate'] = position_rate


