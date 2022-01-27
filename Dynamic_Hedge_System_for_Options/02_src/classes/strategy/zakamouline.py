#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/7 13:01
# @Author  : Hao Wu
# @File    : .py
import pandas as pd
import numpy as np
from .strategyBase import StrategyBase
from scipy import stats as st

class Zakamouline(StrategyBase):

    def __init__(self, gamma=0.5, _lambda=0.00005):
        super().__init__()
        self.gamma = gamma
        self._lambda = _lambda

    def reset_paras(self, gamma=None, _lambda=None):
        self.gamma = gamma if gamma is not None else self.gamma
        self._lambda = _lambda if _lambda is not None else self._lambda

    def calculate_hedge_position(self, greek_df, basic_paras_df, **kwargs):
        # greek_df = greek_df.reset_index()
        self.df_hedge = pd.DataFrame(data=None, columns=['H0', 'H1', 'delta', 'up_bound', 'low_bound'])
        self.df_hedge.loc[:, 'H0'] = self._lambda/(self.gamma*basic_paras_df.loc[:, 'stock_price']*np.power(basic_paras_df.loc[:, 'sigma'], 2) * \
                                                   basic_paras_df.loc[:, 'left_times'])

        self.df_hedge.loc[:,'H1'] = 1.12*np.power(self._lambda, 0.31) * \
                               np.power(basic_paras_df.loc[:, 'left_times'], 0.05) * \
                               np.power((np.exp(-kwargs['r']*basic_paras_df.loc[:, 'left_times'])/basic_paras_df.loc[:, 'sigma']), 0.25) * \
                               np.power(greek_df.loc[:, 'gamma']/self.gamma, 0.5)

        self.df_hedge.loc[:,'K'] = -4.76*np.power(self._lambda,0.78)/\
                              np.power(basic_paras_df.loc[:,'left_times'],0.02)*\
                              np.power((np.exp(-kwargs['r']*basic_paras_df.loc[:,'left_times'])/basic_paras_df.loc[:,'sigma']),0.25)*\
                              np.power(self.gamma*np.power(basic_paras_df.loc[:,'stock_price'],2)*np.abs(greek_df.loc[:,'gamma']),0.15)

        self.df_hedge.loc[:,'adjust_sigma_T'] = basic_paras_df.loc[:,'sigma_T']*np.sqrt(1+self.df_hedge.loc[:,'K'])
        self.df_hedge.loc[:, 'adjust_d1'] = (np.log(basic_paras_df.loc[:, 'stock_price']/kwargs['K'])+kwargs['r']*basic_paras_df.loc[:, 'left_times'])/\
                                       self.df_hedge.loc[:,'adjust_sigma_T']+0.5*self.df_hedge.loc[:,'adjust_sigma_T']
        self.df_hedge.loc[:,'adjust_delta'] = st.norm.cdf(self.df_hedge.loc[:,'adjust_d1'])
        self.df_hedge.loc[:,'delta'] = greek_df.loc[:,'delta']
        self.df_hedge.loc[:,'up_bound'] = self.df_hedge.loc[:,'adjust_delta'] + self.df_hedge.loc[:,'H1']+self.df_hedge.loc[:,'H0']
        self.df_hedge.loc[:,'low_bound'] = self.df_hedge.loc[:,'adjust_delta'] - self.df_hedge.loc[:,'H1']-self.df_hedge.loc[:,'H0']
        position = self.df_hedge['delta'][0]*kwargs['size']//100*100
        position_rate = self.df_hedge['delta'][0]
        for i in range(self.df_hedge.shape[0]):
            if position_rate < self.df_hedge['low_bound'][i] or position_rate > self.df_hedge['up_bound'][i]:
                position = self.df_hedge['delta'][i]*kwargs['size']//100*100
                position_rate = position/kwargs['size']
            self.df_hedge.loc[self.df_hedge.index[i], 'position'] = position
            self.df_hedge.loc[self.df_hedge.index[i], 'position_rate'] = position_rate

    def get_hedge_df(self):
        return self.df_hedge.loc[:, ['delta', 'adjust_delta', 'up_bound', 'low_bound', 'position', 'position_rate']]
