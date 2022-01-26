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
    future_weight_dict = dict().fromkeys(['code_list', 'weight_info'])

    def __init__(self):
        self.reset()

    def reset(self):
        self.future = None
        self.stock_index_name = None
        self.multiplier = None
        self.future_data = None
        self.clear_future_weight_dict()
        self.future_delta = None
        self.target_delta = None

    def clear_future_weight_dict(self):
        self.future_weight_dict['code_list'] = None
        self.future_weight_dict['weight_info'] = None

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

    def get_option_info(self, option): #传入的Option_Contract对象
        self.set_paras(option.stock_index_code)
        self.trade_dates = option.trade_dates
        self.portfolio_position = option.portfolio_position
        self.option_greek_df = option.get_greek_df()
        self.public_df = option.public_df
        self.init_future_weight()
        self.single_option_info = dict()
        for i in range(len(option.option_basket)):
            option_obj = option.option_basket[i]['option_obj']
            option_pos = option.option_basket[i]['option_pos']
            option_class = option.option_basket[i]['option_class']
            greek_df = option_obj.greek_df #这里的greek_df是最开始的optionBase/vanilla里有啥就有啥
            option_r = option_obj.r
            option_K = option_obj.K
            left_times = greek_df['left_times']
            self.single_option_info[i] = {'option_class':option_class,'option_pos':option_pos,'greek_df':greek_df,'r':option_r,'K':option_K,
                                          'left_times':left_times}
        return self

    def init_future_weight(self):
        # self.future_weight_dict['code_list'] = sorted(list(set((self.future_data['month_code'].loc[self.trade_dates]).values.ravel())))
        self.future_weight_dict['code_list'] = self.future_data['month_code'].loc[self.trade_dates].drop(['{0:s}_S.CFE'.format(self.future)], axis=1)
        self.future_weight_dict['weight_info'] = pd.DataFrame(0,index=self.trade_dates, columns=self.future_data['open'].columns)

    @abstractmethod
    def get_hedging_position(self,greek_df,stock_index_price):
        pass

    @abstractmethod
    def calculate_target_delta(self):
        pass

    @abstractmethod
    def calculate_future_weight(self):
        pass

    def get_future_weight(self):
        self.calculate_future_weight()
        return self.future_weight_dict['weight_info']

    def get_target_delta(self):
        self.calculate_target_delta()
        return self.target_delta
