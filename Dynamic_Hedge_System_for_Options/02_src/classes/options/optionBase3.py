"""
@Author: Carl
@Time: 2022/1/22 11:34
@SoftWare: PyCharm
@File: optionBase3.py
"""
import pandas as pd
import numpy as np
from abc import abstractmethod
from datetime import datetime, timedelta as td
from ..basicData.basicData import BasicData
from scipy import stats as st
import matplotlib.pyplot as plt

class OptionBase:
    basic_paras_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price']
    base_type = {
        'VanillaCall': 'Vanilla', 'VanillaPut': 'Vanilla',
        'BullCallSpread': 'OptionPortfolio', 'BearCallSpread': 'OptionPortfolio',
        'BullPutSpread': 'OptionPortfolio', 'BearPutSpread': 'OptionPortfolio',
        'Strangle': 'OptionPortfolio', 'ButterflySpread': 'OptionPortfolio',
    }

    def __init__(self):
        self.reset_paras()
        self.all_trade_dates = BasicData.basicData['close'].index.to_list()
        # self.decompose_df = pd.DataFrame(data=None, columns=['option_value_change', 'delta_value', 'theta_value', 'gamma_value',
        #                                                      'vega_value', 'high_order_value'])
        self.greek_df = pd.DataFrame(data=None, columns=['delta', 'gamma', 'vega', 'theta', 'option_price', 'cash_delta',
                                                         'cash_gamma', 'pos_vega', 'cash_theta', 'option_value'])

    def reset_paras(self):
        self.option_type = None
        self.notional = None
        self.stock_code = None
        self.start_date = None
        self.start_price = None
        self.end_date = None
        self.r = 0.04
        self.K = None
        self.H = None
        self.trade_dates = None
        self.look_back_num = 30

    def set_paras_by_dict(self, para_dict):
        self.parameters = para_dict
        self.set_basic_paras(para_dict)
        self.set_specific_paras(para_dict)

    def set_basic_paras(self, para_dict):
        self.set_option_type(para_dict.get('option_type'))
        self.set_notional(para_dict.get('notional'))
        self.set_start_date(para_dict.get('start_date'))
        self.set_end_date(para_dict.get('end_date'))
        self.set_r(para_dict.get('r'))
        self.set_stock_code(para_dict.get('stock_code'))
        self.set_start_price(para_dict.get('start_price'))
        self.set_look_back_num(para_dict.get('look_back_num'))
        self.set_stock_num()

    def set_specific_paras(self, para_dict):
        if self.base_type[self.option_type] == 'Vanilla':
            self.set_K(para_dict.get('K'))
        elif self.base_type[self.option_type] == 'OptionPortfolio':
            self.set_K(para_dict.get('K'))
        # elif self.option_type in self.base_type['Barrier']:
        #     self.set_K(para_dict.get('K'))
        #     self.set_H(para_dict.get('H'))
        #   todo

    def set_look_back_num(self, look_back_num=None):
        if look_back_num is not None:
            self.look_back_num = look_back_num

    def set_option_type(self, option_type=None):
        if option_type in self.base_type:
            self.option_type = option_type
        else:
            raise ValueError('Invalid option_type!')

    def set_notional(self, notional=None):
        if notional is not None:
            self.notional = notional

    def set_start_price(self, start_price=None):
        if start_price is not None:
            self.start_price = start_price

    def set_start_date(self, start_date=None):
        if start_date is not None:
            self.start_date = start_date
            if self.end_date is not None:
                self.calculate_trade_dates()

    def set_end_date(self, end_date=None):
        if end_date is not None:
            self.end_date = end_date
            if self.start_date is not None:
                self.calculate_trade_dates()

    def set_K(self, K=None):
        if K is not None:
            self.K = K

    def set_r(self, r=None):
        if r is not None:
            self.r = r

    def set_option_fee(self, option_fee=None):
        if option_fee is not None:
            self.option_fee = option_fee

    def set_stock_code(self, stock_code=None):
        if stock_code is not None:
            self.stock_code = stock_code

    def set_H(self, H=None):
        if H is not None:
            self.H = H

    def set_stock_num(self):
        if self.start_price is not None:
            self.stock_num = self.notional / self.start_price

    def calculate_trade_dates(self):
        start_idx = self.all_trade_dates.index(self.start_date)
        end_idx = self.all_trade_dates.index(self.end_date) + 1
        self.trade_dates = self.all_trade_dates[start_idx:end_idx]
        self.look_back_date = self.all_trade_dates[start_idx - self.look_back_num]
        self.look_back_dates = self.all_trade_dates[start_idx - self.look_back_num:end_idx]
        self.trade_dates_length = len(self.trade_dates)

    @abstractmethod
    def calculate_greeks(self):
        pass

    def get_stock_prices(self):
        if self.stock_code is None:
            print('股票代码未设定')
            return -1
        self.stock_prices = BasicData.basicData['close'].loc[self.look_back_dates, self.stock_code]

    def calculate_basic_paras(self):
        self.get_stock_prices()
        self.basic_paras_df = pd.DataFrame(data=None, columns=self.basic_paras_columns)
        self.calculate_vols()
        self.calculate_other_paras()

    def calculate_vols(self):
        vol = self.stock_prices.pct_change().rolling(self.look_back_num).std() * np.sqrt(252)
        self.basic_paras_df.loc[:, 'sigma'] = vol.dropna()

    def calculate_other_paras(self):
        self.basic_paras_df.loc[:, 'left_days'] = np.linspace(self.trade_dates_length - 1, 0.0001, self.trade_dates_length)
        self.basic_paras_df.loc[:, 'left_times'] = self.basic_paras_df.loc[:, 'left_days'] / 252
        self.basic_paras_df.loc[:, 'sigma_T'] = self.basic_paras_df.loc[:, 'sigma'] * np.sqrt(self.basic_paras_df.loc[:, 'left_times'])
        self.basic_paras_df.loc[:, 'stock_price'] = self.stock_prices.loc[self.trade_dates]

    # def calculate_return_decomposition(self):
    #     self.decompose_df.loc[:, 'option_value_change'] = self.greek_df.loc[:, 'option_value'].diff().fillna(0)
    #     self.decompose_df.loc[:, 'delta_value'] = self.greek_df.loc[:, 'delta'] * self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0) * self.stock_num
    #     self.decompose_df.loc[:, 'gamma_value'] = self.greek_df.loc[:, 'gamma'] * 0.5 * self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0) ** 2 * self.stock_num
    #     self.decompose_df.loc[:, 'theta_value'] = self.greek_df.loc[:, 'theta'] / 252 * self.stock_num
    #     self.decompose_df.loc[self.decompose_df.index[0], 'theta_value'] = 0
    #     self.decompose_df.loc[:, 'vega_value'] = self.greek_df.loc[:, 'vega'] * self.basic_paras_df.loc[:, 'sigma'].diff().fillna(0) * self.stock_num
    #     self.decompose_df.loc[:, 'high_order_value'] = self.decompose_df.loc[:, 'option_value_change'] - self.decompose_df.loc[:, 'delta_value']\
    #                                                - self.decompose_df.loc[:,'gamma_value'] - self.decompose_df.loc[:,'theta_value'] - self.decompose_df.loc[:,'vega_value']
    #
    # def calculate_decomposition(self):
    #     if self.greek_df.empty:
    #         self.calculate_greeks()
    #     self.calculate_return_decomposition()
    #
    # def decomposition_vis(self):
    #     if self.decompose_df.empty:
    #         self.calculate_return_decomposition()
    #     df_plot = self.decompose_df.copy()
    #     df_plot.index = np.linspace(len(self.decompose_df)/252, 0, len(self.decompose_df))
    #     fig, ax1 = plt.subplots(figsize=(15, 10))
    #     ax1.set_xlabel('Time')
    #     ax1.set_ylabel('Delta')
    #     ax1.legend(loc='upper left')
    #     ax1.invert_xaxis()
    #     df_plot.loc[:, ['option_value_change', 'delta_value', 'gamma_value', 'theta_value', 'vega_value']].cumsum().plot(ax=ax1)
    #     plt.show()

    def get_greek_df(self):
        self.calculate_greeks()
        return self.greek_df