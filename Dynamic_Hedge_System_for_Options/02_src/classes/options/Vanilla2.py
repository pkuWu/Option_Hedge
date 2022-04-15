"""
@Author: Carl
@Time: 2022/1/22 13:47
@SoftWare: PyCharm
@File: Vanilla2.py
"""
from .optionBase3 import OptionBase
import pandas as pd
import numpy as np
from scipy import stats as st
from abc import abstractmethod

class Vanilla(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_vanilla_paras(self):
        self.calculate_basic_paras()
        self.basic_paras_df.loc[:, 'd1'] = (np.log(self.basic_paras_df.loc[:, 'stock_price']/self.K)+self.r*self.basic_paras_df.loc[:, 'left_times'])/self.basic_paras_df.loc[:,'sigma_T']+0.5*self.basic_paras_df.loc[:,'sigma_T']
        self.basic_paras_df.loc[:, 'd2'] = self.basic_paras_df.loc[:, 'd1'] - self.basic_paras_df.loc[:, 'sigma_T']
        self.basic_paras_df.loc[:, 'nd1'] = st.norm.pdf(self.basic_paras_df.loc[:, 'd1'])
        self.basic_paras_df.loc[:, 'Nd1'] = st.norm.cdf(self.basic_paras_df.loc[:, 'd1'])
        self.basic_paras_df.loc[:, 'Nd2'] = st.norm.cdf(self.basic_paras_df.loc[:, 'd2'])

    @abstractmethod
    def calculate_greeks(self):
        pass

class VanillaCall(Vanilla):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        self.calculate_vanilla_paras()
        self.greek_df.loc[:, 'delta'] = self.basic_paras_df.loc[:, 'Nd1']
        self.greek_df.loc[:, 'gamma'] = self.basic_paras_df.loc[:, 'nd1']/self.basic_paras_df.loc[:, 'stock_price']/self.basic_paras_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'option_price'] = self.basic_paras_df.loc[:, 'stock_price']*self.basic_paras_df.loc[:, 'Nd1']-self.K*np.exp(-self.r*self.basic_paras_df.loc[:, 'left_times'])*self.basic_paras_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.basic_paras_df.loc[:, 'stock_price']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.basic_paras_df.loc[:, 'stock_price'], 2)*self.notional/self.start_price/100
        self.greek_df.loc[:, 'vega'] = self.basic_paras_df.loc[:, 'nd1']*self.basic_paras_df.loc[:, 'stock_price']*np.sqrt(self.basic_paras_df.loc[:, 'left_times'])
        self.greek_df.loc[:, 'pos_vega'] = self.greek_df.loc[:, 'vega']*self.notional/self.start_price
        self.greek_df.loc[:, 'theta'] = -self.basic_paras_df.loc[:, 'stock_price']*self.basic_paras_df.loc[:, 'nd1']*\
                                        self.basic_paras_df.loc[:,'sigma']/2/np.sqrt(self.basic_paras_df.loc[:, 'left_times'])-\
                                        self.r*self.K*np.exp(-self.r*self.basic_paras_df.loc[:, 'left_times'])*self.basic_paras_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'cash_theta'] = self.greek_df.loc[:, 'theta']/252*self.notional/self.start_price
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.notional/self.start_price


class VanillaPut(Vanilla):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        self.calculate_vanilla_paras()
        self.greek_df.loc[:, 'delta'] = self.basic_paras_df.loc[:, 'Nd1']-1
        self.greek_df.loc[:, 'gamma'] = self.basic_paras_df.loc[:, 'nd1']/self.basic_paras_df.loc[:, 'stock_price']/self.basic_paras_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'vega'] = self.basic_paras_df.loc[:, 'nd1']*self.basic_paras_df.loc[:, 'stock_price']*np.sqrt(self.basic_paras_df.loc[:, 'left_times'])
        self.greek_df.loc[:, 'theta'] = -self.basic_paras_df.loc[:, 'stock_price']*self.basic_paras_df.loc[:, 'nd1']*\
                                        self.basic_paras_df.loc[:,'sigma']/2/np.sqrt(self.basic_paras_df.loc[:, 'left_times'])-\
                                        self.r*self.K*np.exp(-self.r*self.basic_paras_df.loc[:, 'left_times'])*(self.basic_paras_df.loc[:, 'Nd2']-1)
        self.greek_df.loc[:, 'option_price'] = self.basic_paras_df.loc[:, 'stock_price']*(self.basic_paras_df.loc[:, 'Nd1']-1)-self.K*np.exp(-self.r*self.basic_paras_df.loc[:, 'left_times'])*(self.basic_paras_df.loc[:, 'Nd2']-1)
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.basic_paras_df.loc[:, 'stock_price']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.basic_paras_df.loc[:, 'stock_price'],2)*self.notional/self.start_price/100
        self.greek_df.loc[:, 'pos_vega'] = self.greek_df.loc[:, 'vega']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_theta'] = self.greek_df.loc[:, 'theta']/252*self.notional/self.start_price
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.notional/self.start_price