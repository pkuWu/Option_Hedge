from classes.options.Option_Contract import Option_Contract
from .Month_Strategy import *
from .Delta_Strategy import *
from ..basicData.basicData import BasicData
import pandas as pd


class Combinator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.multiplier = None
        self.trade_dates = None
        self.future = None
        self.stock_index_name = None
        self.future_delta = None
        self.future_weight = None
        self.future_code_list = None
        self.target_delta = None
        self.option_obj = None
        self.month_obj = None
        self.delta_obj = None

    def get_option(self, option):# option为Option_Contract对象
        self.option_obj = option
        return self

    def set_month_strategy(self, month_strategy):
        self.month_obj = eval(month_strategy)().get_option_info(self.option_obj)
        self.get_future_info()
        self.future_weight = self.month_obj.get_future_weight()
        self.future_code_list = self.month_obj.get_future_code_list()

    def set_delta_strategy(self, delta_strategy):
        self.delta_obj = eval(delta_strategy)().get_option_info(self.option_obj)
        self.target_delta = self.delta_obj.get_target_delta()

    def set_hedge_strategy(self, month_strategy, delta_strategy):
        self.set_month_strategy(month_strategy)
        self.set_delta_strategy(delta_strategy)

    def get_future_info(self):
        if self.month_obj is not None:
            self.future = self.month_obj.future
            self.stock_index_name = self.month_obj.stock_index_name
            self.multiplier = self.month_obj.multiplier
            self.trade_dates = self.month_obj.trade_dates

    def calculate_future_position(self):
        self.future_delta = self.month_obj.get_future_delta()
        self.future_position = round(self.future_weight.mul(self.target_delta, axis=0)/self.future_delta, 0)

    def get_future_position(self):
        self.calculate_future_position()
        return self.future_position