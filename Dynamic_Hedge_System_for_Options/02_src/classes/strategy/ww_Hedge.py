#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/7 17:07
# @Author  : Hao Wu
# @File    : .py
import pandas as pd
import numpy as np
from .strategyBase import StrategyBase


class WW_Hedge(StrategyBase):
    
    def __init__(self,gamma=0.5, _lambda=0.00005):
        super().__init__()
        self.gamma = gamma
        self._lambda = _lambda

    def reset_paras(self, gamma=None, _lambda=None):
        self.gamma = gamma if gamma is not None else self.gamma
        self._lambda = _lambda if _lambda is not None else self._lambda

    def calculate_hedge_position(self, greek_df, basic_paras_df, **kwargs):
        self.df_hedge = pd.DataFrame(columns=['H0', 'H1', 'delta', 'up_bound', 'low_bound'])
        self.df_hedge.loc[:, 'stock_price'] = basic_paras_df.loc[:, 'stock_price']
        self.df_hedge.loc[:, 'H0'] = (3/2*np.exp(-kwargs['r']*basic_paras_df.loc[:, 'left_times'])*self._lambda * \
                                      basic_paras_df.loc[:,'stock_price']*greek_df.loc[:,'gamma']**2/self.gamma)**(1/3)
        self.df_hedge.loc[:, 'delta'] = greek_df.loc[:, 'delta']
        self.df_hedge.loc[:, 'up_bound'] = self.df_hedge.loc[:, 'delta'] + self.df_hedge.loc[:, 'H0']
        self.df_hedge.loc[:, 'low_bound'] = self.df_hedge.loc[:, 'delta'] - self.df_hedge.loc[:, 'H0']
        position = self.df_hedge['delta'][0]*kwargs['size']//100*100
        position_rate = self.df_hedge.loc[:, 'delta'][0]
        for i in range(self.df_hedge.shape[0]):
            if position_rate < self.df_hedge['low_bound'][i] or position_rate > self.df_hedge['up_bound'][i]:
                position = self.df_hedge['delta'][i]*kwargs['size']//100*100
                position_rate = position/kwargs['size']
            self.df_hedge.loc[self.df_hedge.index[i], 'position'] = position
            self.df_hedge.loc[self.df_hedge.index[i], 'position_rate'] = position_rate

    def get_hedge_df(self):
        return self.df_hedge.loc[:, ['delta', 'up_bound', 'low_bound', 'position', 'position_rate']]


