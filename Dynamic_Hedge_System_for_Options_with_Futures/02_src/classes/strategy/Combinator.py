from classes.options.Option_Contract import Option_Contract
from .Month_Strategy import *
from .Delta_Strategy import *
from ..basicData.basicData import BasicData
import pandas as pd


class Combinator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.stock_index_code = None
        self.portfolio_position = None
        self.multiplier = None
        self.trade_dates = None
        self.future = None
        self.future_price = None
        self.stock_index_name = None
        self.future_delta = None
        self.future_weight = None
        self.future_code_list = None
        self.target_delta = None
        self.month_obj = None
        self.delta_obj = None
        self.option_basket = None
        self.greek_df = None
        self.public_df = None

    def get_option(self, stock_index_code, trade_dates, portfolio_position, option_basket, greek_df, public_df):
        self.stock_index_code = stock_index_code
        self.trade_dates = trade_dates
        self.portfolio_position = portfolio_position
        self.option_basket =option_basket
        self.greek_df = greek_df
        self.public_df = public_df
        return self

    def set_month_strategy(self, month_strategy):
        self.month_obj = eval(month_strategy)().get_option_info(self.stock_index_code, self.trade_dates)
        self.get_future_info()
        self.future_weight = self.month_obj.get_future_weight()
        self.future_code_list = self.month_obj.future_weight_dict['code_list']
        self.future_price = self.month_obj.future_data['close'].loc[self.trade_dates]

    def set_delta_strategy(self, delta_strategy):
        self.delta_obj = eval(delta_strategy)().get_option_info(self.portfolio_position, self.option_basket, self.greek_df, self.public_df)
        self.target_delta = self.delta_obj.get_target_delta()

    def set_hedge_strategy(self, month_strategy, delta_strategy):
        self.set_month_strategy(month_strategy)
        self.set_delta_strategy(delta_strategy)

    def get_future_info(self):
        if self.month_obj is not None:
            self.future = self.month_obj.future
            self.stock_index_name = self.month_obj.stock_index_name
            self.multiplier = self.month_obj.multiplier

    def calculate_future_position(self):
        self.future_delta = self.month_obj.get_future_delta()
        self.future_position = round(self.future_weight.mul(self.target_delta, axis=0)/self.future_delta, 0)

    def get_future_position(self):
        self.calculate_future_position()
        return self.future_position