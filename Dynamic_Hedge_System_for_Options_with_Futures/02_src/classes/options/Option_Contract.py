from .Vanilla import VanillaCall,VanillaPut
from ..basicData.basicData import BasicData
import pandas as pd

class OptionContract:
    all_trade_dates = BasicData.ALL_TRADE_DATES
    price_dict = BasicData.PRICE_DICT

    def __init__(self):
        self.public_columns = ['sigma','left_days','left_times','sigma_T','stock_index_price']
        self.greek_columns = ['cash_delta', 'cash_gamma', 'cash_theta', 'option_value']
        self.option_basket = []
        self.reset()

    def reset(self):
        self.notional = 0
        self.stock_index_code = None
        self.start_date = None
        self.end_date = None
        self.option_fee = 0
        self.trade_dates = None

    def add_option_by_dict(self,option_class,option_position,option_paras):
        # Vanilla
        if option_class == 'VanillaCall' or option_class == 'VanillaPut':
            option_dict = self.add_vanilla_option_by_dict(option_class,option_position,option_paras)
            self.get_paras_from_current_option(option_dict['option_obj'])
            self.init_public_greek_df()
            self.update_paras(option_dict)
            self.option_basket.append(option_dict)
            self.get_vanilla_info()
        # elif option_class == 'BullSpreadCall' or option_class == 'BullSpreadPut'
        # 用看涨期权构造的牛市差价
        elif option_class == 'BullSpreadCall':
            option_para_dict1 = {'notional':option_paras['notional'],
                                 'start_date':option_paras['start_date'],
                                 'end_date':option_paras['end_date'],
                                 'K':option_paras['K_low'],
                                 'option_fee':option_paras['option_fee'],
                                 'stock_index_code':option_paras['stock_index_code'],
                                 'start_price':option_paras['start_price']}
            option_para_dict2 = {'notional': option_paras['notional'],
                                 'start_date': option_paras['start_date'],
                                 'end_date': option_paras['end_date'],
                                 'K': option_paras['K_high'],
                                 'option_fee': option_paras['notional'],
                                 'stock_index_code': option_paras['stock_index_code'],
                                 'start_price': option_paras['start_price']}
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall',option_position*1, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position*(-1),option_para_dict2)
            self.get_paras_from_current_option(option_dict1['option_obj'])
            self.init_public_greek_df()
            self.update_paras(option_dict1)
            self.update_paras(option_dict2)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_bullspread_option_info()
        # 用看跌期权构造的牛市差价
        elif option_class == 'BullSpreadPut':
            option_para_dict1 = {'notional':option_paras['notional'],
                                 'start_date':option_paras['start_date'],
                                 'end_date':option_paras['end_date'],
                                 'K':option_paras['K_low'],
                                 'option_fee':option_paras['option_fee'],
                                 'stock_index_code':option_paras['stock_index_code'],
                                 'start_price':option_paras['start_price']}
            option_para_dict2 = {'notional': option_paras['notional'],
                                 'start_date': option_paras['start_date'],
                                 'end_date': option_paras['end_date'],
                                 'K': option_paras['K_high'],
                                 'option_fee': option_paras['notional'],
                                 'stock_index_code': option_paras['stock_index_code'],
                                 'start_price': option_paras['start_price']}
            option_dict1 = self.add_vanilla_option_by_dict('VanillaPut',option_position*1, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut', option_position*(-1),option_para_dict2)
            self.get_paras_from_current_option(option_dict1['option_obj'])
            self.init_public_greek_df()
            self.update_paras(option_dict1)
            self.update_paras(option_dict2)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_bullspread_option_info()
        # 熊市差价
        # Combination
        # 碟式差价

    def add_vanilla_option_by_dict(self,option_class,option_position,option_paras):
        '''
        :param option_paras:
            notional
            start_date
            end_date
            K
            r
            option_fee
            stock_index_code
            start_price
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
        self.option_info = '期权类型:{0:s}，名义金额:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，执行价:{4:,.2f}'.format(
            self.option_name, self.notional, self.stock_index_code, self.option_fee, self.strike_price)

    def get_bullspread_option_info(self):
        option_class = str(type(self.option_basket[0]['option_obj'])).strip("'>").split('.')[-1]
        option_pos = self.option_basket[0]['option_pos']
        if option_class == 'VanillaCall':
            self.option_name = '牛市看涨价差'
        else:
            self.option_name = '牛市看跌价差'
        self.strike_price1 = self.option_basket[0]['option_obj'].K
        self.strike_price2 = self.option_basket[1]['option_obj'].K
        self.option_info = '期权类型:{0:s}，名义金额:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，低执行价:{4:,.2f}，高执行价:{5:,.2f}'.format(\
            self.option_name, self.notional, self.stock_index_code, self.option_fee, self.strike_price1,self.strike_price2)

    def get_paras_from_current_option(self,option):
        self.stock_index_code = option.stock_index_code
        self.start_date = option.start_date
        self.end_date = option.end_date
        self.trade_dates = option.trade_dates
        self.notional = option.notional
        self.option_fee = option.option_fee
        self.public_df = pd.DataFrame(index=self.trade_dates, columns=self.public_columns)
        self.public_df.loc[:,:] = option.greek_df.loc[:,['sigma','left_days','left_times','sigma_T','stock_index_price']]

    def init_public_greek_df(self):
        self.greek_df = pd.DataFrame(0, index=self.trade_dates, columns=self.greek_columns)

    def update_paras(self,option):
        '''
        :param option:
            option_pos
            option_obj
        '''
        self.greek_df.loc[:,:] += (option['option_pos'])*option['option_obj'].greek_df.loc[:,['cash_delta', 'cash_gamma', 'cash_theta', 'option_value']]

    def get_greeks(self):
        return self.greek_df