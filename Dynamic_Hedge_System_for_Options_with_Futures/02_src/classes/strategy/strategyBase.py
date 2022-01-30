import pandas as pd
import numpy as np
from abc import abstractmethod
from classes.basicData.basicData import BasicData
from classes.options.Option_Contract import Option_Contract


class StrategyBase:
    all_trade_dates = BasicData.ALL_TRADE_DATES
    MULTIPLIER = {'000300.SH': 300,
                  '000016.SH': 300,
                  '000905.SH': 200}

    def __init__(self):
        self.reset()

    def reset(self):
        self.future = None
        self.stock_index_name = None
        self.multiplier = None
        self.future_data = None
        self.future_delta = None
        self.target_delta = None
        self.trade_dates = None

    def set_paras(self, stock_index_code=None):
        self.set_future(stock_index_code)
        self.set_stock_index_name(stock_index_code)
        self.get_multiplier(stock_index_code)
        self.set_future_data()

    def set_future(self, stock_index_code=None):
        if stock_index_code == '000300.SH':
            self.future = 'IF'
        elif stock_index_code == '000016.SH':
            self.future = 'IH'
        elif stock_index_code == '000905.SH':
            self.future = 'IC'

    def set_stock_index_name(self, stock_index_code=None):
        if stock_index_code == '000300.SH':
            self.stock_index_name = '沪深300'
        elif stock_index_code == '000016.SH':
            self.stock_index_name = '上证50'
        elif stock_index_code == '000905.SH':
            self.stock_index_name = '中证500'

    def get_multiplier(self, stock_index_code=None):
        if stock_index_code is not None:
            self.multiplier = self.MULTIPLIER[stock_index_code]

    def set_future_data(self):
        self.future_data = BasicData.FUTURE_DATA[self.future]

    def calculate_future_delta(self):
        self.future_delta = self.future_data['close'].loc[self.trade_dates] * self.multiplier

    def get_future_delta(self):
        self.calculate_future_delta()
        return self.future_delta

    @abstractmethod
    def get_hedging_position(self,greek_df,stock_index_price):
        pass

    @abstractmethod
    def get_option_info(self):
        pass
