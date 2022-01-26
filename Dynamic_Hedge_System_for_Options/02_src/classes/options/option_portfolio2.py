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

class OptionPortfolio(OptionBase):
    def __init__(self):
        super().__init__()
        self.options = list()

    def calculate_greeks(self):
        self.calculate_basic_paras()
        self.get_option_list()
        for i, element in enumerate(self.options):
            if i == 0:
                element.get('option_object').calculate_greeks()
                self.greek_df = element.get('option_object').get_greek_df() * element.get('option_position')
            else:
                self.greek_df += element.get('option_object').get_greek_df() * element.get('option_position')

    @abstractmethod
    def get_option_list(self):
        pass

class Strangle(OptionPortfolio):
    def __init__(self):
        super().__init__()
        self.option_list = list()

    def get_option_list(self):
        option1 = VanillaPut()
        parameter = self.parameters.copy()
        parameter['K'] = min(self.K)
        option1.set_paras_by_dict(parameter)
        self.options.append({'option_object': option1, 'option_position': 1})
        option2 = VanillaCall()
        parameter['K'] = max(self.K)
        option2.set_paras_by_dict(parameter)
        self.options.append({'option_object': option2, 'option_position': 1})


    def temp(self):
        pass





