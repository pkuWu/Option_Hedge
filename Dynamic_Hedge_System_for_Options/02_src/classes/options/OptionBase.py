import pandas as pd
import numpy as np
from abc import abstractmethod
from datetime import datetime, timedelta as td
from ..basicData.basicData import BasicData
from scipy import stats as st


class OptionBase:
    # %% 初始化
    all_trade_dates = BasicData.basicData['trade_dates']
    price_dict = BasicData.PRICE_DICT
    greek_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price']
    base_type = {'Vanilla': ['call', 'put'],
                      'Barrier': ['cuo', 'cui', 'cdo', 'cdi', 'puo', 'pui', 'pdo', 'pdi'],
                      'OptionPortfolio': []}
    def __init__(self):
        self.reset_paras()

    def reset_paras(self):
        self.option_type = None
        self.notional = None
        self.stock_code = None
        self.start_date = None
        self.start_price = None
        self.end_date = None
        self.look_back_date = None
        self.K = None
        self.r = 0.04
        self.H = None
        self.option_fee = None
        self.trade_dates = None
        self.look_back_num = 60

    # def set_paras(self,notional=None,start_date=None,end_date=None,K=None,r=None,option_fee=None,stock_code=None,start_price=None,look_back_num=None):
    #     self.set_notional(notional)
    #     self.set_start_date(start_date)
    #     self.set_end_date(end_date)
    #     self.set_K(K)
    #     self.set_r(r)
    #     self.set_option_fee(option_fee)
    #     self.set_stock_code(stock_code)
    #     self.set_start_price(start_price)
    #     self.set_look_back_num(look_back_num)

    def set_look_back_num(self, look_back_num=None):
        if look_back_num is not None:
            self.look_back_num = look_back_num

    def set_paras_by_dict(self, para_dict):
        self.set_notional(para_dict.get('notional'))
        self.set_start_date(para_dict.get('start_date'))
        self.set_end_date(para_dict.get('end_date'))
        self.set_K(para_dict.get('K'))
        self.set_r(para_dict.get('r'))
        self.set_option_fee(para_dict.get('option_fee'))
        self.set_stock_code(para_dict.get('stock_code'))
        self.set_start_price(para_dict.get('start_price'))
        self.set_look_back_num(para_dict.get('look_back_num'))
        self.set_H(para_dict.get('H'))
        self.set_option_type(para_dict.get('option_type'))
        self.set_stock_num()

    def set_option_type(self, option_type=None):
        if option_type is not None:
            self.option_type = option_type

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

    def set_H(self, H=None):
        if H is not None:
            self.H = H

    def set_stock_num(self):
        if self.start_price is not None:
            self.stock_num = self.notional / self.start_price

    def calculate_trade_dates(self):
        start_idx = self.all_trade_dates.index(self.start_date)
        end_idx = self.all_trade_dates.index(self.end_date) + 1
        self.trade_dates = self.all_trade_dates[start_idx:end_idx]
        self.look_back_date = self.all_trade_dates[start_idx - self.look_back_num]
        self.look_back_dates = self.all_trade_dates[start_idx - self.look_back_num:end_idx]
        self.trade_dates_length = len(self.trade_dates)

    @abstractmethod
    def calculate_greeks(self):
        pass

    def get_stock_prices(self):
        if self.stock_code is None:
            print('股票代码未设定')
            return -1
        self.stock_prices = self.price_dict['close'].loc[self.look_back_dates, self.stock_code]

    def calculate_basic_paras(self):
        self.get_stock_prices()
        self.greek_df = pd.DataFrame(index=self.trade_dates, columns=self.greek_columns)
        self.calculate_vols()
        self.calculate_other_paras()
        if self.option_type in self.base_type.get('Barrier'):
            self.calculate_barrier_paras()
            if ((self.H <= self.K) & (self.base_type in ['cui', 'cdo'])) | (
                    (self.H > self.K) & (self.base_type in ['cuo', 'cdi'])):
                self.calculate_vanilla_paras()
            # elif self.H > self.K and self.base_type in ['cuo', 'cdi']:
            #     self.calculate_vanilla_paras()
        elif self.option_type in self.base_type.get('Vanilla'):
            self.calculate_vanilla_paras()

    def calculate_vols(self):
        vol = self.stock_prices.pct_change().rolling(self.look_back_num).std() * np.sqrt(252)
        self.greek_df.loc[:, 'sigma'] = vol.dropna()

    def calculate_other_paras(self):
        self.greek_df.loc[:, 'left_days'] = np.linspace(self.trade_dates_length - 1, 0.0001, self.trade_dates_length)
        self.greek_df.loc[:, 'left_times'] = self.greek_df.loc[:, 'left_days'] / 252
        self.greek_df.loc[:, 'sigma_T'] = self.greek_df.loc[:, 'sigma'] * np.sqrt(self.greek_df.loc[:, 'left_times'])
        self.greek_df.loc[:, 'stock_price'] = self.stock_prices.loc[self.trade_dates]

    def calculate_vanilla_paras(self):
        self.greek_df.loc[:, 'd1'] = (np.log(self.greek_df.loc[:, 'stock_price']/self.K)+self.r*self.greek_df.loc[:, 'left_times'])/self.greek_df.loc[:,'sigma_T']+0.5*self.greek_df.loc[:,'sigma_T']
        self.greek_df.loc[:, 'd2'] = self.greek_df.loc[:, 'd1'] - self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'nd1'] = st.norm.pdf(self.greek_df.loc[:, 'd1'])
        self.greek_df.loc[:, 'Nd1'] = st.norm.cdf(self.greek_df.loc[:, 'd1'])
        self.greek_df.loc[:, 'Nd2'] = st.norm.cdf(self.greek_df.loc[:, 'd2'])

    def calculate_barrier_paras(self):
        self.greek_df.loc[:, 'Lambda'] = self.r/self.greek_df.loc[:, 'sigma']**2 + 0.5
        self.greek_df.loc[:, 'y'] = np.log(self.H**2/(self.greek_df.loc[:, 'stock_price']))/self.greek_df.loc[:, 'sigma_T'] + self.greek_df.loc[:, 'Lambda']*self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'xi'] = np.log(self.greek_df.loc[:, 'stock_price']/self.H)/self.greek_df.loc[:, 'sigma_T'] + self.greek_df.loc[:, 'Lambda']*self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'yi'] = np.log(self.H/self.greek_df.loc[:, 'stock_price'])/self.greek_df.loc[:, 'sigma_T'] + self.greek_df.loc[:, 'Lambda']*self.greek_df.loc[:, 'sigma_T']

    def calculate_return_decomposition(self):
        self.greek_df.loc[:,'option_value_change'] = self.greek_df[:,'option_value'].diff().fillna(0)
        self.greek_df.loc[:,'delta_value'] = self.greek_df[:,'delta']*self.greek_df[:,'stock_price'].diff().fillna(0)*self.stock_num
        self.greek_df.loc[:,'gamma_value'] = self.greek_df[:,'gamma']*0.5*self.greek_df[:,'stock_price'].diff().fillna(0)**2*self.stock_num
        self.greek_df.loc[:,'theta_value'] = self.greek_df[:,'theta']/252*self.stock_num
        self.greek_df.loc[0,'theta_value'] = 0
        self.greek_df.loc[:,'vega_value'] = self.greek_df[:,'vega']*self.greek_df.loc[:,'sigma'].diff().fillna(0)*self.stock_num


    def calculate_decomposition(self):
        self.calculate_greeks()
        self.calculate_return_decomposition()