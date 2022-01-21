#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/7 17:07
# @Author  : Hao Wu
# @File    : .py
import pandas as pd
import numpy as np
from .strategyBase import StrategyBase


class WW_Hedge(StrategyBase):
    df_hedge_columns = ['stock_price', 'H0','delta','up_bound','low_bound']
    
    def __init__(self,gamma=0.5,lamda=0.00005):
        super().__init__()
        self.gamma = gamma
        self.lamda = lamda

    # def reset_paras(self):
    #     self.gamma = 0.5
    #     self.Lambda = 0.00005
    #
    # def set_paras(self,gamma=None,Lambda=None):
    #     self.set_gamma(gamma)
    #     self.set_Lambda(Lambda)
    #
    # def set_gamma(self,gamma=None):
    #     if gamma is not None:
    #         self.gamma = gamma
    #
    # def set_Lambda(self,Lambda=None):
    #     if Lambda is not None:
    #         self.Lambda = Lambda

    def get_hedging_position(self,greek_df,**kwargs):
        # kwargs= {'r':r,'lambda':lambda,'size':size,'gamma':gamma}
        # size = notional/start_price
        # self.set_paras(kwargs.get('gamma'),kwargs.get('Lambda'))
        greek_df = greek_df.reset_index()
        self.df_hedge = pd.DataFrame(columns=self.df_hedge_columns)
        self.df_hedge.loc[:, 'stock_price'] = greek_df.loc[:, 'stock_price']
        self.df_hedge.loc[:, 'H0'] = (3/2*np.exp(-kwargs['r']*greek_df.loc[:, 'left_times'])*self.lamda*greek_df.loc[:,'stock_price']*greek_df.loc[:,'gamma']**2/self.gamma)**(1/3)
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
        return self.df_hedge


