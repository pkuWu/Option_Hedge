from .strategyBase import StrategyBase
from abc import abstractmethod
import pandas as pd


class Month_StrategyBase(StrategyBase):
    future_weight_dict = dict().fromkeys(['code_list', 'weight_info'])

    def __init__(self):
        super().__init__()
        self.clear_future_weight_dict()

    def clear_future_weight_dict(self):
        self.future_weight_dict['code_list'] = None
        self.future_weight_dict['weight_info'] = None

    def get_option_info(self, stock_index_code, trade_dates):
        self.set_paras(stock_index_code)
        self.trade_dates = trade_dates
        self.init_future_weight()
        return self

    def init_future_weight(self):
        # self.future_weight_dict['code_list'] = sorted(list(set((self.future_data['month_code'].loc[self.trade_dates]).values.ravel())))
        self.future_weight_dict['code_list'] = self.future_data['month_code'].loc[self.trade_dates].drop(['{0:s}_S.CFE'.format(self.future)], axis=1)
        self.future_weight_dict['weight_info'] = pd.DataFrame(0,index=self.trade_dates, columns=self.future_data['open'].columns)

    @abstractmethod
    def calculate_future_weight(self):
        pass

    def get_future_weight(self):
        self.calculate_future_weight()
        return self.future_weight_dict['weight_info']