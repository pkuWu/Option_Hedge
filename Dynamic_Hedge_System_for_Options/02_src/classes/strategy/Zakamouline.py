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
    def __init__(self):
        super(Zakamouline, self).__init__()

    def reset_paras(self):
        self.gamma = None
        self.Lambda = None

    def set_paras(self,gamma=None,Lambda=None):
        self.set_gamma(gamma)
        self.set_Lambda(Lambda)

    def set_gamma(self,gamma=None):
        if gamma is not None:
            self.gamma = gamma

    def set_Lambda(self,Lambda=None):
        if Lambda is not None:
            self.Lambda = Lambda

    def get_hedging_position(self,greek_df,**kwargs):
        # kwargs= {'r':r,'lambda':lambda,'size':size,'K':K}
        # size = notional/start_price
        self.set_paras(kwargs['gamma'],kwargs['Lambda'])
        greek_df = greek_df.reset_index()
        self.df_hedge = pd.DataFrame(columns=['H0','H1','delta','up_bound','low_bound'])
        self.df_hedge.loc[:,'H0'] = kwargs['Lambda']/(kwargs['gamma']*greek_df.loc[:,'stock_price']*np.power(greek_df.loc[:,'sigma'],2)*greek_df.loc[:,'left_times'])

        self.df_hedge.loc[:,'H1'] = 1.12*np.power(kwargs['Lambda'],0.31)*\
                               np.power(greek_df.loc[:,'left_times'],0.05)*\
                               np.power((np.exp(-kwargs['r']*greek_df.loc[:,'left_times'])/greek_df.loc[:,'sigma']),0.25)*\
                               np.power(greek_df.loc[:,'gamma']/kwargs['gamma'],0.5)

        self.df_hedge.loc[:,'K'] = -4.76*np.power(kwargs['Lambda'],0.78)/\
                              np.power(greek_df.loc[:,'left_times'],0.02)*\
                              np.power((np.exp(-kwargs['r']*greek_df.loc[:,'left_times'])/greek_df.loc[:,'sigma']),0.25)*\
                              np.power(kwargs['gamma']*np.power(greek_df.loc[:,'stock_price'],2)*np.abs(greek_df.loc[:,'gamma']),0.15)

        self.df_hedge.loc[:,'adjust_sigma_T'] = greek_df.loc[:,'sigma_T']*np.sqrt(1+self.df_hedge.loc[:,'K'])
        self.df_hedge.loc[:, 'adjust_d1'] = (np.log(greek_df.loc[:, 'stock_price']/kwargs['K'])+kwargs['r']*greek_df.loc[:, 'left_times'])/\
                                       self.df_hedge.loc[:,'adjust_sigma_T']+0.5*self.df_hedge.loc[:,'adjust_sigma_T']
        self.df_hedge.loc[:,'adjust_delta'] = st.norm.cdf(self.df_hedge.loc[:,'adjust_d1'])
        self.df_hedge.loc[:,'delta'] = greek_df.loc[:,'cash_delta']
        self.df_hedge.loc[:,'up_bound'] = self.df_hedge.loc[:,'adjust_delta'] + self.df_hedge.loc[:,'H1']+self.df_hedge.loc[:,'H0']
        self.df_hedge.loc[:,'low_bound'] = self.df_hedge.loc[:,'adjust_delta'] - self.df_hedge.loc[:,'H1']-self.df_hedge.loc[:,'H0']
        position = 0
        position_rate = self.df_hedge.loc[0,'delta']
        for i in range(0,self.df_hedge.shape[0]):
            if position_rate<self.df_hedge.loc[i,'low_bound'] or position_rate>self.df_hedge.loc[i,'up_bound']:
                position = self.df_hedge.loc[i,'delta']*kwargs['size']//100*100
                position_rate = position/kwargs['size']
            self.df_hedge.loc[i, 'position'] = position
            self.df_hedge.loc[i,'position_rate'] = position_rate
        return self.df_hedge
