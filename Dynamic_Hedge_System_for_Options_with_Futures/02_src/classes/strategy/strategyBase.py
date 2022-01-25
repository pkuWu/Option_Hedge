import pandas as pd
from abc import abstractmethod
from ..basicData.basicData import BasicData
from classes.options.Option_Contract import Option_Contract


class StrategyBase:
    all_trade_dates = BasicData.ALL_TRADE_DATES
    MULTIPLIER = {'000300.SH': 300,
                  '000016.SH': 300,
                  '000905.SH': 200}
    future_weight_dict = dict().fromkeys(['code_list', 'weight_info'])

    def __init__(self):
        self.target_delta = None # 需要对冲的delta（Hedge_ALL，Hedge_Half, WW，ZM算出来的）
        self.reset()

    def reset(self):
        self.future = None
        self.multiplier = None
        self.future_data = None
        self.clear_future_weight_dict()

    def clear_future_weight_dict(self):
        self.future_weight_dict['code_list'] = None
        self.future_weight_dict['weight_info'] = None

    def set_paras(self, stock_index_code=None):
        self.set_future(stock_index_code)
        self.get_multiplier(stock_index_code)
        self.set_future_data()

    def set_future(self, stock_index_code=None):
        if stock_index_code == '000300.SH':
            self.future = 'IF'
        elif stock_index_code == '000016.SH':
            self.future = 'IH'
        elif stock_index_code == '000905.SH':
            self.future = 'IC'

    def get_multiplier(self, stock_index_code=None):
        if stock_index_code is not None:
            self.multiplier = self.MULTIPLIER[stock_index_code]

    def set_future_data(self):
        self.future_data = BasicData.FUTURE_DATA[self.future]

    def calculate_future_delta(self):
        pass

    def get_option_info(self, option): #传入的Option_Contract对象
        self.set_paras(option.stock_index_code)
        self.trade_dates = option.trade_dates
        self.option_greek_df = option.get_greek_df()
        self.init_future_weight()
        return self

    def init_future_weight(self):
        # self.future_weight_dict['code_list'] = sorted(list(set((self.future_data['month_code'].loc[self.trade_dates]).values.ravel())))
        self.future_weight_dict['code_list'] = self.future_data['month_code'].loc[self.trade_dates]
        self.future_weight_dict['weight_info'] = pd.DataFrame(0,index=self.trade_dates, columns=self.future_data['open'].columns)

    @abstractmethod
    def get_hedging_position(self,greek_df,stock_price):
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