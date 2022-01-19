#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/1/18 22:23
# @Author  : Hao Wu
# @File    : .py
from .Vanilla import VanillaCall,VanillaPut
from .Barrier import DownInPut,DownOutPut,DownOutCall,DownInCall
import numpy as np
import pandas as pd

class Option_Portfolio:
    greek_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price']
    portfolio_classes = ['BullSpread', 'BearSpread', 'ButterflySpread', 'Strangle']
    def __init__(self):

        self.reset()

    def reset(self):
        self.option_list = [] #每个element是个字典，每个字典有两个key,key1:option_object,key2:option_position


    def create_portfolio_dict(self,**para_dict):
        if para_dict.get('portfolio_class') not in self.portfolio_classes:
            print('')
            return
        if para_dict.get('portfolio_class') == 'BullSpread':
            Option_para_dict1 = {'notional':para_dict.get('notional'),
                                 'start_date':para_dict.get('start_date'),
                                 'end_date':para_dict.get('end_date'),
                                 'K':para_dict.get('K_low'),
                                 'Option_fee':para_dict.get('Option_fee'),
                                 'stock_code':para_dict.get('stock_code'),
                                 'start_price':para_dict.get('start_price'),
                                 'option_type':para_dict.get('option_type1'),
                                 'position':para_dict.get('position')}
            Option_para_dict2 = {'notional':para_dict.get('notional'),
                                 'start_date':para_dict.get('start_date'),
                                 'end_date':para_dict.get('end_date'),
                                 'K':para_dict.get('K_high'),
                                 'Option_fee':para_dict.get('Option_fee'),
                                 'stock_code':para_dict.get('stock_code'),
                                 'start_price':para_dict.get('start_price'),
                                 'option_type':para_dict.get('option_type2')
                                 } #放到另一个函数定义里面



