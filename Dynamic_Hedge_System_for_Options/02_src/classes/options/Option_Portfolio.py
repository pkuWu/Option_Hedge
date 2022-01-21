#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/18 22:23
# @Author  : Hao Wu
# @File    : .py
from .Vanilla import VanillaCall,VanillaPut
from ..basicData.basicData import BasicData
from .Barrier import DownInPut,DownOutPut,DownOutCall,DownInCall
import numpy as np
import pandas as pd

class Option_Portfolio:
    # greek_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price']
    greek_columns = ['delta', 'gamma', 'theta', 'vega']
    portfolio_classes = ['CallSpread', 'PutSpread', 'ButterflySpread', 'Strangle']
    def __init__(self):
        self.reset()
        self.all_trade_dates = BasicData.basicData['close'].index.to_list()

    def reset(self):
        self.option_list = []
        self.option_para = [] #每个element是个字典，每个字典有两个key,key1:option_object,key2:option_position
    #
    # def get_Spread_para_dict(self,**para_dict):
    #     """
    #     :param para_dict:
    #     :portfolio_class:
    #     :notional:
    #     :start_date:
    #     :end_date:
    #     :K_low:
    #     :K_high:
    #     :Option_fee:
    #     :stock_code:
    #     :start_price:
    #     :position1:
    #     :position2:
    #     """
    #     Option_para_dict1 = {'notional': para_dict.get('notional'),
    #                          'start_date': para_dict.get('start_date'),
    #                          'end_date': para_dict.get('end_date'),
    #                          'K': para_dict.get('K_low'),
    #                          'Option_fee': para_dict.get('Option_fee'),
    #                          'stock_code': para_dict.get('stock_code'),
    #                          'start_price': para_dict.get('start_price'),
    #                          'position': para_dict.get('position1')}
    #
    #     Option_para_dict2 = {'notional': para_dict.get('notional'),
    #                          'start_date': para_dict.get('start_date'),
    #                          'end_date': para_dict.get('end_date'),
    #                          'K': para_dict.get('K_high'),
    #                          'Option_fee': para_dict.get('Option_fee'),
    #                          'stock_code': para_dict.get('stock_code'),
    #                          'start_price': para_dict.get('start_price'),
    #                          'position':para_dict.get('position2')
    #                          }
    #     return Option_para_dict1, Option_para_dict2

    def get_Spread_para_dict(self, **para_dict):
        Option_para_dict1 = {'notional': para_dict.get('notional'),
                             'start_date': para_dict.get('start_date'),
                             'end_date': para_dict.get('end_date'),
                             'K': para_dict.get('K_low'),
                             'stock_code': para_dict.get('stock_code'),
                             'start_price': para_dict.get('start_price')
                             }

        Option_para_dict2 = Option_para_dict1.copy()
        Option_para_dict2['K'] = para_dict.get('K_high')
        return Option_para_dict1, Option_para_dict2

    def create_portfolio_dict(self, **para_dict):

        if para_dict.get('portfolio_class') not in self.portfolio_classes:
            raise ValueError('option_portfolio is not found')

        elif para_dict.get('portfolio_class') == 'CallSpread':
             Option_para_dict1, Option_para_dict2 = self.get_Spread_para_dict(**para_dict)
             self.option_para.append(Option_para_dict1)
             self.option_para.append(Option_para_dict2)
             Option_list_element1 = dict({'option_object':VanillaCall(),
                                         'option_position':Option_para_dict1.get('position')})
             self.option_list.append(Option_list_element1)
             Option_list_element2 = dict({'option_object':VanillaCall(),
                                         'option_position':Option_para_dict2.get('position')})
             self.option_list.append(Option_list_element2)

        elif para_dict.get('portfolio_class') == 'PutSpread':
             Option_para_dict1, Option_para_dict2 = self.get_Spread_para_dict(**para_dict)
             self.option_para.append(Option_para_dict1)
             self.option_para.append(Option_para_dict2)
             Option_list_element1 = dict({'option_object':VanillaPut(),
                                         'option_position':Option_para_dict1.get('position')})
             self.option_list.append(Option_list_element1)
             Option_list_element2 = dict({'option_object':VanillaPut(),
                                         'option_position':Option_para_dict2.get('position')})
             self.option_list.append(Option_list_element2)

        elif para_dict.get('portfolio_class') == 'ButterflySpread':
            Option_para_dict1, Option_para_dict2 = self.get_Spread_para_dict(**para_dict)
            Option_para_dict3 = Option_para_dict1.copy()
            Option_para_dict3['K'] = Option_para_dict1.get('K') + (Option_para_dict2.get('K')-Option_para_dict1.get('K'))/2.0
            self.option_para.append(Option_para_dict1)
            self.option_para.append(Option_para_dict2)
            self.option_para.append(Option_para_dict3)
            Option_list_element1 = dict({'option_object': VanillaCall(),
                                         'option_position': 1})
            Option_list_element2 = dict({'option_object': VanillaCall(),
                                         'option_position': 1})
            Option_list_element3 = dict({'option_object': VanillaCall(),
                                         'option_position': -2})
            self.option_list.append(Option_list_element1)
            self.option_list.append(Option_list_element2)
            self.option_list.append(Option_list_element3)

        elif para_dict.get('portfolio_class') == 'Strangle':
             Option_para_dict1, Option_para_dict2 = self.get_Spread_para_dict(**para_dict)
             self.option_para.append(Option_para_dict1)
             self.option_para.append(Option_para_dict2)
             Option_list_element1 = dict({'option_object':VanillaPut(),
                                         'option_position': 1})
             self.option_list.append(Option_list_element1)
             Option_list_element2 = dict({'option_object': VanillaCall(),
                                         'option_position': 1})
             self.option_list.append(Option_list_element2)

    def calculate_portfolio_greeks(self):
        start_date = self.option_para[0].get('start_date')
        start_idx = self.all_trade_dates.index(start_date)
        end_date = self.option_para[0].get('end_date')
        end_idx = self.all_trade_dates.index(end_date) + 1 # ？
        trade_index = self.all_trade_dates[start_idx:end_idx]

        self.df_portfolio_greeks = pd.DataFrame(index=trade_index, columns=self.greek_columns)

        result=0
        for i,element in enumerate(self.option_list):
            element.get('option_object').set_paras_by_dict(self.option_para[i])
            element.get('option_object').calculate_greeks()
            result += \
                element.get('option_object').return_result().loc[:, self.greek_columns]*element.get('option_position')
        self.df_portfolio_greeks.loc[:, self.greek_columns] = result

    def return_result(self):
        return self.df_portfolio_greeks






