from .OptionBase import OptionBase
import pandas as pd
import numpy as np
from scipy import stats as st
class VanillaCall(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        self.calculate_basic_paras()
        self.greek_df.loc[:, 'delta'] = self.greek_df.loc[:, 'Nd1']
        self.greek_df.loc[:, 'gamma'] = self.greek_df.loc[:, 'nd1']/self.greek_df.loc[:, 'stock_index_price']/self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'theta'] = -self.greek_df.loc[:, 'stock_index_price']*self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:,'sigma']/2/np.sqrt(self.greek_df.loc[:, 'left_times'])-self.r*self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*self.greek_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'option_price'] = self.greek_df.loc[:, 'stock_index_price']*self.greek_df.loc[:, 'Nd1']-self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*self.greek_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.greek_df.loc[:, 'stock_index_price']*self.multiplier
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.greek_df.loc[:, 'stock_index_price'],2)*self.multiplier/100
        self.greek_df.loc[:, 'cash_theta'] = self.greek_df.loc[:, 'theta']/252*self.multiplier
        self.greek_df.loc[:, 'vega'] = self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:, 'stock_index_price']*np.sqrt(self.greek_df.loc[:, 'left_times'])
        # self.greek_df.loc[:, 'pos_vega'] = self.greek_df.loc[:, 'vega']*self.multiplier
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.multiplier

    def return_result(self):
        return self.greek_df

class VanillaPut(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        self.calculate_basic_paras()
        self.greek_df.loc[:, 'delta'] = self.greek_df.loc[:, 'Nd1']-1
        self.greek_df.loc[:, 'gamma'] = self.greek_df.loc[:, 'nd1']/self.greek_df.loc[:, 'stock_index_price']/self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'theta'] = -self.greek_df.loc[:, 'stock_index_price']*self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:,'sigma']/2/np.sqrt(self.greek_df.loc[:, 'left_times'])-self.r*self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*(self.greek_df.loc[:, 'Nd2']-1)
        self.greek_df.loc[:, 'option_price'] = self.greek_df.loc[:, 'stock_index_price']*(self.greek_df.loc[:, 'Nd1']-1)-self.K*np.exp(-self.r*self.greek_df.loc[:, 'left_times'])*(self.greek_df.loc[:, 'Nd2']-1)
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.greek_df.loc[:, 'stock_index_price']*self.multiplier
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.greek_df.loc[:, 'stock_index_price'],2)*self.multiplier/100
        self.greek_df.loc[:, 'cash_theta'] = self.greek_df.loc[:, 'theta']/252*self.multiplier
        self.greek_df.loc[:, 'vega'] = self.greek_df.loc[:, 'nd1']*self.greek_df.loc[:, 'stock_index_price']*np.sqrt(self.greek_df.loc[:, 'left_times'])
        # self.greek_df.loc[:, 'pos_vega'] = self.greek_df.loc[:, 'vega']*self.multiplier
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.multiplier

    def get_greek_df(self):
        return self.greek_df