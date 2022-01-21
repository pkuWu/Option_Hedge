from .Vanilla import VanillaCall,VanillaPut
from ..basicData.basicData import BasicData
import pandas as pd


class Option_Contract:
    all_trade_dates = BasicData.ALL_TRADE_DATES
    price_dict = BasicData.PRICE_DICT
    public_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_index_price']
    greek_columns = ['cash_delta', 'cash_gamma', 'cash_theta', 'option_value']

    def __init__(self):
        self.reset()

    def reset(self):
        self.option_basket = []
        self.multiplier = 100
        self.stock_index_code = None
        self.start_date = None
        self.end_date = None
        self.option_fee = 0
        self.trade_dates = None

    def create_option_portfolio(self,option_class,option_position,**option_paras):
        # VanillaCall
        if option_class == 'VanillaCall':
            option_dict = self.add_vanilla_option_by_dict(option_class,option_position,option_paras) # option_dict = {'option_obj': ,'option_pos': }
            self.get_paras_from_current_option(option_dict['option_obj'])
            self.option_basket.append(option_dict)
            self.get_vanilla_info()
        elif option_class == 'VanillaPut':
            option_dict = self.add_vanilla_option_by_dict(option_class,option_position,option_paras)
            self.get_paras_from_current_option(option_dict['option_obj'])
            self.option_basket.append(option_dict)
            self.get_vanilla_info()
        self.init_public_greek_df()
        self.calculate_portfolio_greek_df(self.option_basket)

    def add_vanilla_option_by_dict(self,option_class,option_position,option_paras):
        '''
        :param option_paras:
            multiplier
            start_date
            end_date
            K
            r
            option_fee
            stock_index_code
        '''
        option_dict = dict().fromkeys(['option_obj','option_pos'])
        option_dict['option_obj'] = eval(option_class)()
        option_dict['option_obj'].set_paras_by_dict(option_paras)
        option_dict['option_pos'] = option_position
        option_dict['option_obj'].calculate_greeks()
        return option_dict

    def get_vanilla_info(self):
        self.option_name = str(type(self.option_basket[0]['option_obj'])).strip("'>").split('.')[-1]
        self.strike_price = self.option_basket[0]['option_obj'].K
        self.option_info = '期权类型:{0:s}，合约乘数:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，执行价:{4:,.2f}'.format(
            self.option_name, self.multiplier, self.stock_index_code, self.option_fee, self.strike_price)

    def get_paras_from_current_option(self,option):
        self.stock_index_code = option.stock_index_code
        self.start_date = option.start_date
        self.end_date = option.end_date
        self.trade_dates = option.trade_dates
        self.multiplier = option.multiplier
        self.option_fee = option.option_fee
        self.public_df = pd.DataFrame(index=self.trade_dates, columns=self.public_columns)
        self.public_df.loc[:,:] = option.greek_df.loc[:,['sigma','left_days','left_times','sigma_T','stock_index_price']]

    def init_public_greek_df(self):
        self.greek_df = pd.DataFrame(0, index=self.trade_dates, columns=self.greek_columns)

    def calculate_portfolio_greek_df(self,option_basket):
        for option_dict in option_basket:
            self.greek_df.loc[:, :] += (option_dict['option_pos']) * option_dict['option_obj'].greek_df.loc[:,['cash_delta', 'cash_gamma', 'cash_theta','option_value']]

    def get_greek_df(self):
        return self.greek_df