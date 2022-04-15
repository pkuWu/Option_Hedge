import pandas as pd
from abc import abstractmethod
from datetime import datetime, timedelta as td
from ..basicData.basicData import BasicData

class OptionBase2:
    # %% 初始化
    all_trade_dates = BasicData.ALL_TRADE_DATES
    price_dict = BasicData.PRICE_DICT

    def __init__(self):
        self.reset_paras()
        self.greek_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price', 'd1', 'nd1', 'Nd1', 'Nd2',
                              'delta', 'gamma', 'vega', 'theta', 'option_price', 'cash_delta', 'cash_gamma',
                              'cash_theta', 'option_value']

    def reset_paras(self):
        self.notional = None
        self.stock_code = None
        self.start_date = None
        self.end_date = None
        self.look_back_date = None
        self.K = None
        self.r = 0.04
        self.option_fee = None
        self.trade_dates = None
        self.trade_datetimes = None

    def set_paras(self, notional=None, start_date=None, end_date=None, K=None, r=None, option_fee=None, stock_code=None,
                  start_price=None):
        self.set_notional(notional)
        self.set_start_date(start_date)
        self.set_end_date(end_date)
        self.set_K(K)
        self.set_r(r)
        self.set_option_fee(option_fee)
        self.set_stock_code(stock_code)
        self.set_start_price(start_price)

    def set_paras_by_dict(self, para_dict):
        self.set_notional(para_dict.get('notional'))
        self.set_start_date(para_dict.get('start_date'))
        self.set_end_date(para_dict.get('end_date'))
        self.set_K(para_dict.get('K'))
        self.set_r(para_dict.get('r'))
        self.set_option_fee(para_dict.get('option_fee'))
        self.set_stock_code(para_dict.get('stock_code'))
        self.set_start_price(para_dict.get('start_price'))

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

    def calculate_trade_dates(self):
        start_idx = self.all_trade_dates.index(self.start_date)
        end_idx = self.all_trade_dates.index(self.end_date) + 1
        self.trade_dates = self.all_trade_dates[start_idx:end_idx]
        self.look_back_date = self.all_trade_dates[start_idx - 60]
        self.look_back_dates = self.all_trade_dates[start_idx - 60:end_idx]
        self.trade_datetimes = sorted(
            [datetime(x.year, x.month, x.day, 9, 30) for x in self.trade_dates] + [datetime(x.year, x.month, x.day, 15)
                                                                                   for x in self.trade_dates])
        self.look_back_datetimes = sorted([datetime(x.year, x.month, x.day, 9, 30) for x in self.look_back_dates] + [
            datetime(x.year, x.month, x.day, 15) for x in self.look_back_dates])
        self.datetime_length = len(self.trade_datetimes)

    @abstractmethod
    def calculate_greeks(self):
        pass

    def get_stock_prices(self):
        if self.stock_code is None:
            print('股票代码未设定')
            return -1
        open_price = self.price_dict['open'].loc[self.look_back_dates, self.stock_code]
        close_price = self.price_dict['close'].loc[self.look_back_dates, self.stock_code]
        open_price.index = open_price.index + td(hours=9, minutes=30)
        close_price.index = close_price.index + td(hours=15)
        self.stock_prices = pd.concat([open_price, close_price], axis=0).sort_index()