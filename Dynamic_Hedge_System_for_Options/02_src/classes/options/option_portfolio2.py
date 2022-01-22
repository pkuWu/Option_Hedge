"""
@Author: Carl
@Time: 2022/1/22 10:53
@SoftWare: PyCharm
@File: option_portfolio2.py
"""
from .Vanilla2 import VanillaCall, VanillaPut
from .optionBase3 import OptionBase
from abc import abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class OptionPortfolio:
    def __init__(self):
        self.decompose_df = pd.DataFrame(data=None, columns=['option_value_change', 'delta_value', 'theta_value', 'gamma_value',
                                                             'vega_value', 'high_order_value'])
        self.option_list = []

    def get_option_list(self, para_dict):
        self.option_type = para_dict.get('option_type')
        self.stock_num = para_dict.get('notional') / para_dict.get('start_price')

        if self.option_type in ['VanillaCall', 'VanillaPut']:
            option = eval(self.option_type)()
            option.set_paras_by_dict(para_dict)
            self.option_list.append({'option_object': option, 'option_position': 1})
        elif para_dict.get('option_type') == 'Strangle':
            option1 = VanillaPut()
            parameter = para_dict.copy()
            parameter['K'] = min(para_dict.get('K'))
            option1.set_paras_by_dict(parameter)
            self.option_list.append({'option_object': option1, 'option_position': 1})
            option2 = VanillaCall()
            parameter['K'] = max(para_dict.get('K'))
            option2.set_paras_by_dict(parameter)
            self.option_list.append({'option_object': option2, 'option_position': 1})


    def calculate_greeks(self):
        for i, element in enumerate(self.option_list):
            if i == 0:
                self.greek_df = element.get('option_object').get_greek_df() * element.get('option_position')
            else:
                self.greek_df += element.get('option_object').get_greek_df() * element.get('option_position')

        self.basic_paras_df = self.option_list[0].get('option_object').basic_paras_df

    def calculate_return_decomposition(self):
        self.decompose_df.loc[:, 'option_value_change'] = self.greek_df.loc[:, 'option_value'].diff().fillna(0)
        self.decompose_df.loc[:, 'delta_value'] = self.greek_df.loc[:, 'delta'] * self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0) * self.stock_num
        self.decompose_df.loc[:, 'gamma_value'] = self.greek_df.loc[:, 'gamma'] * 0.5 * self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0) ** 2 * self.stock_num
        self.decompose_df.loc[:, 'theta_value'] = self.greek_df.loc[:, 'theta'] / 252 * self.stock_num
        self.decompose_df.loc[self.decompose_df.index[0], 'theta_value'] = 0
        self.decompose_df.loc[:, 'vega_value'] = self.greek_df.loc[:, 'vega'] * self.basic_paras_df.loc[:, 'sigma'].diff().fillna(0) * self.stock_num
        self.decompose_df.loc[:, 'high_order_value'] = self.decompose_df.loc[:, 'option_value_change'] - self.decompose_df.loc[:, 'delta_value']\
                                                   - self.decompose_df.loc[:,'gamma_value'] - self.decompose_df.loc[:,'theta_value'] - self.decompose_df.loc[:,'vega_value']

    def calculate_decomposition(self):
        if self.greek_df.empty:
            self.calculate_greeks()
        self.calculate_return_decomposition()

    def decomposition_vis(self):
        if self.decompose_df.empty:
            self.calculate_return_decomposition()
        df_plot = self.decompose_df.copy()
        df_plot.index = np.linspace(len(self.decompose_df)/252, 0, len(self.decompose_df))
        fig, ax1 = plt.subplots(figsize=(15, 10))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Delta')
        ax1.invert_xaxis()
        df_plot.loc[:, ['option_value_change', 'delta_value', 'gamma_value', 'theta_value', 'vega_value']].cumsum().plot(ax=ax1)
        plt.show()

    def get_greek_df(self):
        self.calculate_greeks()
        return self.greek_df



# class OptionPortfolio(OptionBase):
#     def __init__(self):
#         super().__init__()
#         self.options = list()
#
#     def calculate_greeks(self):
#         self.calculate_basic_paras()
#         self.get_option_list()
#         for i, element in enumerate(self.options):
#             if i == 0:
#                 element.get('option_object').calculate_greeks()
#                 self.greek_df = element.get('option_object').get_greek_df() * element.get('option_position')
#             else:
#                 self.greek_df += element.get('option_object').get_greek_df() * element.get('option_position')
#
#     @abstractmethod
#     def get_option_list(self):
#         pass
#
# class Strangle(OptionPortfolio):
#     def __init__(self):
#         super().__init__()
#
#     def get_option_list(self):
#         option1 = VanillaPut()
#         parameter = self.parameters.copy()
#         parameter['K'] = min(self.K)
#         option1.set_paras_by_dict(parameter)
#         self.options.append({'option_object': option1, 'option_position': 1})
#         option2 = VanillaCall()
#         parameter['K'] = max(self.K)
#         option2.set_paras_by_dict(parameter)
#         self.options.append({'option_object': option2, 'option_position': 1})


