""" 
@Time    : 2022/1/3 19:46
@Author  : Carl
@File    : SingleBarrier.py
@Software: PyCharm
"""
from .OptionBase import OptionBase
import pandas as pd
import numpy as np
from scipy import stats as st
from .Vanilla import VanillaPut, VanillaCall

class DownOutCall(OptionBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def bs_method(K, r, H, left_times, sigma_T, stock_price, Lambda, xi, yi):
        return (stock_price * st.norm.cdf(xi)) - K * np.exp(-r * left_times) * st.norm.cdf(xi - sigma_T) - \
                stock_price * (H/stock_price) ** (2 * Lambda) * st.norm.cdf(yi) + K * np.exp(-r * left_times) * (H/stock_price) ** (2 * Lambda - 2) * st.norm.cdf(yi - sigma_T)

    def calculate_greeks(self):
        if self.H >= self.K:
            # self.greek_df['option_price'] = self.greek_df.loc[:, 'stock_price'] * st.norm.cdf(self.greek_df[:, 'xi']) - self.K * np.exp(-self.r*self.greek_df.loc[:, 'left_times']) * st.norm.cdf(self.greek_df.loc[:, 'xi'] - self.greek_df.loc[:, 'sigma_T']) - \
            #     self.greek_df['stock_price'] * (self.H/self.greek_df.loc[:, 'stock_price']) ** (2*self.greek_df.loc[:, 'Lambda']) * st.norm.cdf(self.greek_df.loc[:, 'yi']) + \
            #     self.K * np.exp(-self.r*self.greek_df.loc[:, 'left_times']) * (self.H/self.greek_df.loc[:, 'stock_price']) ** (2*self.greek_df.loc[:, 'Lambda']-2)*st.norm.cdf(self.greek_df.loc[:, 'yi'] - self.greek_df.loc[:, 'sigma_T'])
            self.greek_df['option_price'] = DownOutCall.bs_method(self.K, self.r, self.H,
                                                                  self.greek_df.loc[:, 'left_times'],
                                                                  self.greek_df.loc[:, 'sigma_T'],
                                                                  self.greek_df.loc[:, 'stock_pirce'],
                                                                  self.greek_df.loc[:, 'Lambda'],
                                                                  self.greek_df.loc[:, 'xi'],
                                                                  self.greek_df.loc[:, 'yi'])
        else:
            # self.greek_df.loc[:, 'vanilla_price'] = self.greek_df.loc[:, 'stock_price'] * self.greek_df.loc[:,'Nd1'] - self.K * np.exp(-self.r * self.greek_df.loc[:, 'left_times']) * self.greek_df.loc[:, 'Nd2']
            self.greek_df['option_price'] = VanillaCall.bs_method(self.K, self.r,
                                                                  self.greek_df.loc[:, 'left_times'],
                                                                  self.greek_df.loc[:, 'stock_price'],
                                                                  self.greek_df.loc[:, 'Nd1'],
                                                                  self.greek_df.loc[: 'Nd2']) - \
                                            DownInCall.bs_method(self.K, self.r, self.H,
                                                                 self.greek_df.loc[:, 'left_times'],
                                                                 self.greek_df.loc[:, 'sigma_T'],
                                                                 self.greek_df.loc[:, 'stock_price'],
                                                                 self.greek_df.loc[:, 'Lambda'],
                                                                 self.greek_df.loc[:, 'y'])

        # self.greek_df.loc[:, 'delta'] =
        # self.greek_df.loc[:, 'gamma'] =
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.greek_df.loc[:, 'stock_price']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.greek_df.loc[:, 'stock_price'],2)*self.notional/self.start_price/100
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.notional/self.start_price


class DownInCall(OptionBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def bs_method(K, r, H, left_times, sigma_T, stock_price, Lambda, y):
        return stock_price*(H/stock_price)*st.norm.cdf(y) - K*np.exp(-r*left_times)*(H/stock_price)**(2*Lambda-2)*st.norm.cdf(y-sigma_T)

    def calculate_greeks(self):
        # self.greek_df['option_price'] = self.greek_df.loc[:, 'stock_price'] * (self.H/self.greek_df.loc[:, 'stock_price'])**(2*self.greek_df.loc[:, 'Lambda']) * st.norm.pdf(self.greek_df.loc[:, 'y']) - \
        #     self.K * np.exp(-self.r * self.greek_df.loc[:, 'left_times']) * (self.H/self.greek_df.loc[:, 'stock_price'])**(2*self.greek_df.loc[:, 'Lambda'] - 2) * \
        #     st.norm.pdf(self.greek_df.loc[:, 'y'] - self.greek_df.loc[:, 'sigma_T'])
        if self.H < self.K:
            self.greek_df.loc[:, 'option_price'] = DownInCall.bs_method(self.K, self.r, self.H,
                                                                        self.greek_df.loc[:, 'left_times'],
                                                                        self.greek_df.loc[:, 'sigma_T'],
                                                                        self.greek_df.loc[:, 'stock_price'],
                                                                        self.greek_df.loc[:, 'Lambda'],
                                                                        self.greek_df.loc[:, 'y'])
        else:
            self.greek_df.loc[:, 'option_price'] = VanillaCall.bs_method(self.K, self.r,
                                                                         self.greek_df.loc[:, 'left_times'],
                                                                         self.greek_df.loc[:, 'stock_price'],
                                                                         self.greek_df.loc[:, 'Nd1'],
                                                                         self.greek_df.loc[: 'Nd2']) - \
                                                   DownOutCall.bs_method(self.K, self.r, self.H,
                                                                         self.greek_df.loc[:, 'left_times'],
                                                                         self.greek_df.loc[:, 'sigma_T'],
                                                                         self.greek_df.loc[:, 'stock_pirce'],
                                                                         self.greek_df.loc[:, 'Lambda'],
                                                                         self.greek_df.loc[:, 'xi'],
                                                                         self.greek_df.loc[:, 'yi'])

        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta']*self.greek_df.loc[:, 'stock_price']*self.notional/self.start_price
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma']*np.power(self.greek_df.loc[:, 'stock_price'],2)*self.notional/self.start_price/100
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price']*self.notional/self.start_price

class UpperOutCall(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        pass

class UpperInCall(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        pass

class UpperOutPut(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        pass

class UpperInPut(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        pass

class DownOutPut(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        pass

class DownInPut(OptionBase):
    def __init__(self):
        super().__init__()

    def calculate_greeks(self):
        pass




