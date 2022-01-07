from .OptionBase import OptionBase
import pandas as pd
import numpy as np
from scipy import stats as st
class VanillaCall(OptionBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def bs_method(K, r, left_times, stock_price, Nd1, Nd2):
        return stock_price * Nd1 - K * np.exp(-r*left_times) * Nd2

    def calculate_greeks(self):
        self.calculate_basic_paras()
        self.greek_df.loc[:, 'delta'] = self.greek_df.loc[:, 'Nd1']
        self.greek_df.loc[:, 'gamma'] = self.greek_df.loc[:, 'nd1']/self.greek_df.loc[:, 'stock_price']/self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'option_price'] = self.greek_df.loc[:, 'stock_price']*self.greek_df.loc[:, 'Nd1']-self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*self.greek_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.greek_df.loc[:, 'stock_price']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.greek_df.loc[:, 'stock_price'],2)*self.notional/self.start_price/100
        self.greek_df.loc[:, 'pos_vega'] = self.greek_df.loc[:, 'vega']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_theta'] = self.greek_df.loc[:, 'theta']/252*self.notional/self.start_price
        self.greek_df.loc[:, 'vega'] = self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:, 'stock_price']*np.sqrt(self.greek_df.loc[:, 'left_times'])
        self.greek_df.loc[:, 'theta'] = -self.greek_df.loc[:, 'stock_price']*self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:,'sigma']/2/np.sqrt(self.greek_df.loc[:, 'left_times'])-self.r*self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*self.greek_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.notional/self.start_price

    def calculate_VanillaCall_decomposition(self):
        self.calculate_greeks()
        self.calculate_return_decomposition()

class VanillaPut(OptionBase):
    def __init__(self):
        super().__init__()

    # @staticmethod
    # def bs_method():

    def calculate_greeks(self):
        self.calculate_basic_paras()
        self.greek_df.loc[:, 'delta'] = self.greek_df.loc[:, 'Nd1']-1
        self.greek_df.loc[:, 'gamma'] = self.greek_df.loc[:, 'nd1']/self.greek_df.loc[:, 'stock_price']/self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'option_price'] = self.greek_df.loc[:, 'stock_price']*(self.greek_df.loc[:, 'Nd1']-1)-self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*(self.greek_df.loc[:, 'Nd2']-1)
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.greek_df.loc[:, 'stock_price']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.greek_df.loc[:, 'stock_price'],2)*self.notional/self.start_price/100
        self.greek_df.loc[:, 'pos_vega'] = self.greek_df.loc[:, 'vega']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_theta'] = self.greek_df.loc[:, 'theta']/252*self.notional/self.start_price
        self.greek_df.loc[:, 'vega'] = self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:, 'stock_price']*np.sqrt(self.greek_df.loc[:, 'left_times'])
        self.greek_df.loc[:, 'theta'] = -self.greek_df.loc[:, 'stock_price']*self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:,'sigma']/2/np.sqrt(self.greek_df.loc[:, 'left_times'])-self.r*self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*(self.greek_df.loc[:, 'Nd2']-1)
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.notional/self.start_price

    def calculate_VanillaPut_decomposition(self):
        self.calculate_greeks()
        self.calculate_return_decomposition()