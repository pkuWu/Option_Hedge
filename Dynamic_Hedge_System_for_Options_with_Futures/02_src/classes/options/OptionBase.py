import pandas as pd
import numpy as np
from abc import abstractmethod
from datetime import datetime,timedelta as td
from ..basicData.basicData import BasicData
from scipy import stats as st

class OptionBase:
#%% 初始化
    all_trade_dates = BasicData.ALL_TRADE_DATES
    price_dict = BasicData.PRICE_DICT

    def __init__(self):
        self.reset_paras()
        self.greek_columns = ['sigma','left_days','left_times','sigma_T','stock_index_price','d1', 'nd1', 'Nd1', 'Nd2',
                              'option_price','delta','gamma','theta','cash_delta','cash_gamma','cash_theta','vega','option_value']
        self.option_type = {'vanilla':['call','put'],
                            #待加入：障碍、美式、etc
                            }

    def reset_paras(self):
        self.notional = None
        self.stock_index_code = None
        self.start_date = None
        self.end_date = None
        self.look_back_date = None
        self.K = None
        self.r = 0.04
        self.option_fee = None
        self.trade_dates = None
        self.look_back_num = 60
    
    def set_paras(self,notional=None,start_date=None,end_date=None,K=None,r=None,option_fee=None,stock_index_code=None,start_price=None,look_back_num=None):
        self.set_notional(notional)
        self.set_start_date(start_date)
        self.set_end_date(end_date)
        self.set_K(K)
        self.set_r(r)
        self.set_option_fee(option_fee)
        self.set_stock_index_code(stock_index_code)
        self.set_start_price(start_price)
        self.set_look_back_num(look_back_num)

    def set_look_back_num(self,look_back_num=None):
        if look_back_num is not None:
            self.look_back_num = look_back_num

    def set_paras_by_dict(self,para_dict):
        self.set_notional(para_dict.get('notional'))
        self.set_start_date(para_dict.get('start_date'))
        self.set_end_date(para_dict.get('end_date'))
        self.set_K(para_dict.get('K'))
        self.set_r(para_dict.get('r'))
        self.set_option_fee(para_dict.get('option_fee'))
        self.set_stock_index_code(para_dict.get('stock_index_code'))
        self.set_start_price(para_dict.get('start_price'))
    
    def set_notional(self,notional=None):
        if notional is not None:
            self.notional = notional

    def set_start_price(self,start_price=None):
        if start_price is not None:
            self.start_price = start_price

    def set_start_date(self,start_date=None):
        if start_date is not None:
            self.start_date = start_date
            if self.end_date is not None:
                self.calculate_trade_dates()
    
    def set_end_date(self,end_date=None):
        if end_date is not None:
            self.end_date = end_date
            if self.start_date is not None:
                self.calculate_trade_dates()
    
    def set_K(self,K=None):
        if K is not None:
            self.K = K
    
    def set_r(self,r=None):
        if r is not None:
            self.r = r
            
    def set_option_fee(self,option_fee=None):
        if option_fee is not None:
            self.option_fee = option_fee

    def set_stock_index_code(self,stock_index_code=None):
        if stock_index_code is not None:
            self.stock_index_code = stock_index_code
            
    def calculate_trade_dates(self):
        start = self.all_trade_dates.index(self.start_date)
        end = self.all_trade_dates.index(self.end_date)+1
        self.trade_dates = self.all_trade_dates[start:end]
        self.look_back_date = self.all_trade_dates[start-self.look_back_num]
        self.look_back_dates = self.all_trade_dates[start-self.look_back_num:end]
        self.trade_dates_length = len(self.trade_dates)

    @abstractmethod
    def calculate_greeks(self):
        pass

    def get_stock_index_prices(self):
        if self.stock_index_code is None:
            print('股指代码未设定')
            return -1
        self.stock_index_prices = self.price_dict['close'].loc[self.look_back_dates,self.stock_index_code]

    def calculate_basic_paras(self):
        self.get_stock_index_prices()
        self.greek_df = pd.DataFrame(index=self.trade_dates, columns=self.greek_columns)
        self.calculate_vols()
        self.calculate_other_paras()

    def calculate_vols(self):
        vol = self.stock_index_prices.pct_change().rolling(self.look_back_num).std() * np.sqrt(252)
        self.greek_df.loc[:, 'sigma'] = vol.dropna()

    def calculate_other_paras(self):
        self.greek_df.loc[:, 'left_days'] = np.linspace(self.trade_dates_length-1, 0.0001, self.trade_dates_length)
        self.greek_df.loc[:, 'left_times'] = self.greek_df.loc[:, 'left_days'] / 252
        self.greek_df.loc[:, 'sigma_T'] = self.greek_df.loc[:, 'sigma'] * np.sqrt(self.greek_df.loc[:, 'left_times'])
        self.greek_df.loc[:, 'stock_index_price'] = self.stock_index_prices.loc[self.trade_dates]
        self.greek_df.loc[:, 'd1'] = (np.log(self.greek_df.loc[:, 'stock_index_price']/self.K)+self.r*self.greek_df.loc[:, 'left_times'])/self.greek_df.loc[:,'sigma_T']+0.5*self.greek_df.loc[:,'sigma_T']
        self.greek_df.loc[:, 'd2'] = self.greek_df.loc[:, 'd1'] - self.greek_df.loc[:, 'sigma_T']
        self.greek_df.loc[:, 'nd1'] = st.norm.pdf(self.greek_df.loc[:, 'd1'])
        self.greek_df.loc[:, 'Nd1'] = st.norm.cdf(self.greek_df.loc[:, 'd1'])
        self.greek_df.loc[:, 'Nd2'] = st.norm.cdf(self.greek_df.loc[:, 'd2'])