from .Vanilla import VanillaCall,VanillaPut
from ..basicData.basicData import BasicData
import pandas as pd
import matplotlib.pyplot as plt


class Option_Contract:
    all_trade_dates = BasicData.ALL_TRADE_DATES
    price_dict = BasicData.PRICE_DICT
    public_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_index_price']
    greek_columns = ['delta','gamma','theta', 'vega','cash_delta', 'cash_gamma', 'cash_theta', 'option_value']
    pnl_columns = ['delta_pnl','gamma_pnl','vega_pnl','theta_pnl','option_pnl','high_order_pnl']
    option_type = {'VanillaCall': '看涨期权',
                   'VanillaPut': '看跌期权',
                   'BullCallSpread': '牛市看涨差价',
                   'BullPutSpread': '牛市看跌差价',
                   'BearCallSpread': '熊市看涨差价',
                   'BearPutSpread': '熊市看跌差价',
                   'BoxSpread': '盒式差价',
                   'Straddle': '跨式组合',
                   'Strangle': '宽跨式组合',
                   'ButterflyCallSpread': '蝶式看涨差价',
                   'ButterflyPutSpread': '蝶式看跌差价',
                   'CalendarCallSpread': '看涨期权构造的日历差价',
                   'CalendarPutSpread': '看跌期权构造的日历差价',
                   'RatioCallSpread': '看涨比率差价',# 这里是看涨比率差价空头、看跌比率差价空头
                   'RatioPutSpread': '看跌比率差价'}

    def __init__(self):
        self.reset()

    def reset(self):
        self.option_basket = []
        self.multiplier = None
        self.stock_index_code = None
        self.start_date = None
        self.end_date = None
        self.option_fee = 0
        self.trade_dates = None

    def create_option_portfolio(self,option_class,option_position,**option_paras):
        # VanillaCall
        if option_class == 'VanillaCall':
            option_dict = self.add_vanilla_option_by_dict(option_class,option_position,option_paras) # option_dict = {'option_obj': ,'option_pos': }
            self.option_basket.append(option_dict)
            self.get_paras(option_dict['option_obj'])
            self.get_vanilla_info(option_class)
        # VanillaPut
        elif option_class == 'VanillaPut':
            option_dict = self.add_vanilla_option_by_dict(option_class,option_position,option_paras)
            self.option_basket.append(option_dict)
            self.get_paras(option_dict['option_obj'])
            self.get_vanilla_info(option_class)
        # BullCallSpread
        elif option_class == 'BullCallSpread':
            option_dict1, option_dict2 = self.add_spread_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # BullPutSpread
        elif option_class == 'BullPutSpread':
            option_dict1, option_dict2 = self.add_spread_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # BearCallSpread
        elif option_class == 'BearCallSpread':
            option_dict1, option_dict2 = self.add_spread_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # BearPutSpread
        elif option_class == 'BearPutSpread':
            option_dict1, option_dict2 = self.add_spread_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # BoxSpread
        elif option_class =='BoxSpread':
            option_dict1, option_dict2 = self.add_spread_option_by_dict('BullCallSpread', option_position,option_paras)
            option_dict3, option_dict4 = self.add_spread_option_by_dict('BearPutSpread', option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.option_basket.append(option_dict3)
            self.option_basket.append(option_dict4)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # Straddle
        elif option_class == 'Straddle':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall',option_position,option_paras)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut',option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_vanilla_info(option_class)
        # Strangle
        elif option_class == 'Strangle':
            option_dict1, option_dict2 = self.add_strangle_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # ButterflyCallSpread
        elif option_class == 'ButterflyCallSpread':
            option_dict1, option_dict2, option_dict3 = self.add_butterfly_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_butterfly_info(option_class)
        # ButterflyPutSpread
        elif option_class == 'ButterflyPutSpread':
            option_dict1, option_dict2, option_dict3 = self.add_butterfly_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_butterfly_info(option_class)
        # CalendarCallSpread
        elif option_class == 'CalendarCallSpread':
            option_dict1, option_dict2 = self.add_calendar_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_calendar_info(option_class)
        # CalendarPutSpread
        elif option_class == 'CalendarPutSpread':
            option_dict1, option_dict2 = self.add_calendar_option_by_dict(option_class, option_position,option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_calendar_info(option_class)
        # RatioCallSpread
        elif option_class == 'RatioCallSpread':
            option_dict1, option_dict2 = self.add_ratio_option_by_dict(option_class, option_position, option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        # RatioPutSpread
        elif option_class == 'RatioPutSpread':
            option_dict1, option_dict2 = self.add_ratio_option_by_dict(option_class, option_position, option_paras)
            self.option_basket.append(option_dict1)
            self.option_basket.append(option_dict2)
            self.get_paras(option_dict1['option_obj'])
            self.get_spread_info(option_class)
        self.calculate_portfolio_greek_df(self.option_basket)
        return self

    def add_vanilla_option_by_dict(self,option_class,option_position,option_paras):
        '''
        :param option_paras:
            stock_index_code
            start_date
            end_date
            K
            r
            option_fee
        '''
        option_dict = dict().fromkeys(['option_obj','option_pos'])
        option_dict['option_obj'] = eval(option_class)()
        option_dict['option_obj'].set_paras_by_dict(option_paras)
        option_dict['option_pos'] = option_position
        option_dict['option_obj'].calculate_greeks()
        return option_dict

    def add_spread_option_by_dict(self, option_class, option_position, option_paras):
        option_para_dict1 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_low'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_para_dict2 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_high'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        if option_class == 'BullCallSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall', option_position, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position * (-1), option_para_dict2)
        elif option_class == 'BullPutSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaPut', option_position, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut', option_position * (-1), option_para_dict2)
        elif option_class == 'BearCallSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall', option_position * (-1), option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position, option_para_dict2)
        elif option_class == 'BearPutSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaPut', option_position * (-1), option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut', option_position, option_para_dict2)
        return option_dict1, option_dict2

    def add_strangle_option_by_dict(self, option_class, option_position, option_paras):
        option_para_dict1 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_low'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_para_dict2 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_high'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_dict1 = self.add_vanilla_option_by_dict('VanillaPut', option_position, option_para_dict1)
        option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position, option_para_dict2)
        return option_dict1, option_dict2

    def add_butterfly_option_by_dict(self, option_class, option_position, option_paras):
        option_para_dict1 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_low'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_para_dict2 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_mid'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_para_dict3 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_high'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        if option_class == 'ButterflyCallSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall', option_position, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position * (-2), option_para_dict2)
            option_dict3 = self.add_vanilla_option_by_dict('VanillaCall', option_position, option_para_dict3)
        elif option_class == 'ButterflyPutSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaPut', option_position, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut', option_position * (-2), option_para_dict2)
            option_dict3 = self.add_vanilla_option_by_dict('VanillaPut', option_position, option_para_dict3)
        return option_dict1, option_dict2, option_dict3

    def add_calendar_option_by_dict(self, option_class, option_position, option_paras):
        option_para_dict1 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date_before'],
                             'K': option_paras['K'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_para_dict2 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date_after'],
                             'K': option_paras['K'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        if option_class == 'CalendarCallSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall', option_position * (-1), option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position, option_para_dict2)
        elif option_class == 'CalendarPutSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaPut', option_position * (-1), option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut', option_position, option_para_dict2)
        return option_dict1, option_dict2

    def add_ratio_option_by_dict(self, option_class, option_position, option_paras):
        option_para_dict1 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_low'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        option_para_dict2 = {'stock_index_code': option_paras['stock_index_code'],
                             'start_date': option_paras['start_date'],
                             'end_date': option_paras['end_date'],
                             'K': option_paras['K_high'],
                             'r': option_paras['r'],
                             'option_fee': option_paras['option_fee']}
        factor1, factor2 = self.calculate_position_factor(option_class, option_para_dict1, option_para_dict2)
        if option_class == 'RatioCallSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaCall', option_position * factor1, option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaCall', option_position * factor2 * (-1), option_para_dict2)
        elif option_class == 'RatioPutSpread':
            option_dict1 = self.add_vanilla_option_by_dict('VanillaPut', option_position * factor1 * (-1), option_para_dict1)
            option_dict2 = self.add_vanilla_option_by_dict('VanillaPut', option_position * factor2, option_para_dict2)
        return option_dict1, option_dict2

    def calculate_position_factor(self, option_class, option_para_dict1, option_para_dict2):
        if option_class == 'RatioCallSpread':
            vanilla1 = VanillaCall()
            vanilla2 = VanillaCall()
        elif option_class == 'RatioPutSpread':
            vanilla1 = VanillaPut()
            vanilla2 = VanillaPut()
        vanilla1.set_paras_by_dict(option_para_dict1)
        vanilla2.set_paras_by_dict(option_para_dict2)
        vanilla1.calculate_greeks()
        vanilla2.calculate_greeks()
        delta1 = vanilla1.greek_df.loc[vanilla1.trade_dates[0], 'delta']
        delta2 = vanilla2.greek_df.loc[vanilla2.trade_dates[0], 'delta']
        factor1 = round(abs(delta2) / (abs(delta1) + abs(delta2)), 2)
        factor2 = round(abs(delta1) / (abs(delta1) + abs(delta2)), 2)
        return factor1, factor2

    def get_vanilla_info(self,option_class):
        self.option_class = option_class
        self.option_name = self.option_type[option_class]
        self.strike_price = self.option_basket[0]['option_obj'].K
        self.option_info = '期权类型:{0:s}，合约乘数:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，执行价:{4:,.2f}'.format(
            self.option_name, self.multiplier, self.stock_index_code, self.option_fee, self.strike_price)

    def get_spread_info(self, option_class):
        self.option_class = option_class
        self.option_name = self.option_type[option_class]
        self.strike_price_low = self.option_basket[0]['option_obj'].K
        self.strike_price_high = self.option_basket[1]['option_obj'].K
        self.option_info = '期权类型:{0:s}，合约乘数:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，低执行价:{4:,.2f}，高执行价:{5:,.2f}'.format(
            self.option_name, self.multiplier, self.stock_index_code, self.option_fee, self.strike_price_low, self.strike_price_high)

    def get_butterfly_info(self, option_class):
        self.option_class = option_class
        self.option_name = self.option_type[option_class]
        self.strike_price_low = self.option_basket[0]['option_obj'].K
        self.strike_price_mid = self.option_basket[1]['option_obj'].K
        self.strike_price_high = self.option_basket[2]['option_obj'].K
        self.option_info = '期权类型:{0:s}，合约乘数:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，K1:{4:,.2f}，K2:{5:,.2f},K3:{6:,.2f}'.format(
            self.option_name, self.multiplier, self.stock_index_code, self.option_fee, self.strike_price_low, self.strike_price_mid, self.strike_price_high)

    def get_calendar_info(self, option_class):
        self.option_class = option_class
        self.option_name = self.option_type[option_class]
        self.strike_price = self.option_basket[0]['option_obj'].K
        self.end_date_after = self.option_basket[1]['option_obj'].end_date
        self.option_info = '期权类型:{0:s}，合约乘数:{1:,.0f}，标的:{2:s}，期权费:{3:,.0f}，K:{4:,.2f}，到期日1:{5:s},到期日2:{6:s}'.format(
            self.option_name, self.multiplier, self.stock_index_code, self.option_fee, self.strike_price, str(self.end_date), str(self.end_date_after))

    def get_paras(self, option):
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
        self.init_public_greek_df()
        for option_dict in option_basket:
            self.greek_df.loc[:, :] += (option_dict['option_pos']) * option_dict['option_obj'].greek_df.loc[:, ['delta','gamma','theta', 'vega','cash_delta', 'cash_gamma', 'cash_theta', 'option_value']]

    def get_greek_df(self):
        return self.greek_df

    def init_public_pnl_df(self):
        self.pnl_df = pd.DataFrame(0, index=self.trade_dates, columns=self.pnl_columns)

    def calculate_portfolio_pnl_df(self):
        self.init_public_pnl_df()
        self.pnl_df.loc[:, 'delta_pnl'] = self.greek_df.loc[:, 'delta']*self.public_df.loc[:, 'stock_index_price'].diff().fillna(0)*self.multiplier
        self.pnl_df.loc[:, 'gamma_pnl'] = 0.5*self.greek_df.loc[:, 'gamma'] * self.public_df.loc[:, 'stock_index_price'].diff().fillna(0)**2*self.multiplier
        self.pnl_df.loc[:, 'vega_pnl'] = self.greek_df.loc[:, 'vega']*self.public_df.loc[:, 'sigma'].diff().fillna(0)*self.multiplier
        self.pnl_df.loc[:, 'theta_pnl'] = self.greek_df.loc[:, 'theta']*self.public_df.loc[:, 'left_times'].diff().fillna(0)*self.multiplier
        self.pnl_df.loc[:, 'option_pnl'] = self.greek_df.loc[:, 'option_value'].diff().fillna(0)
        self.pnl_df.loc[:, 'high_order_pnl'] = self.pnl_df.loc[:, 'option_pnl']-self.pnl_df.loc[:, 'delta_pnl']-self.pnl_df.loc[:, 'gamma_pnl']-self.pnl_df.loc[:, 'vega_pnl']-self.pnl_df.loc[:, 'theta_pnl']

    def get_pnl_df(self):
        return self.pnl_df

    def visualize_pnl(self):
        fig, ax = self.init_canvas()
        ax.plot(self.trade_dates, self.pnl_df.loc[:, 'delta_pnl'].cumsum(), label = 'delta_pnl')
        ax.plot(self.trade_dates, self.pnl_df.loc[:, 'gamma_pnl'].cumsum(), label = 'gamma_pnl')
        ax.plot(self.trade_dates, self.pnl_df.loc[:, 'vega_pnl'].cumsum(), label = 'vega_pnl')
        ax.plot(self.trade_dates, self.pnl_df.loc[:, 'theta_pnl'].cumsum(), label = 'theta_pnl')
        ax.plot(self.trade_dates, self.pnl_df.loc[:, 'option_pnl'].cumsum(), label = 'option_pnl')
        ax.plot(self.trade_dates, self.pnl_df.loc[:, 'high_order_pnl'].cumsum(), label = 'high_order_pnl')
        if self.option_class in ['VanillaCall', 'VanillaPut', 'Straddle']:
            ax.set_title('期权类型:{0:s}，标的:{1:s}，期权费:{2:,.0f}，执行价:{3:,.2f}'.format(self.option_name, self.stock_index_code, self.option_fee, self.strike_price), fontsize = 10)
        elif self.option_class in ['BullCallSpread', 'BullPutSpread', 'BearCallSpread', 'BearPutSpread', 'BoxSpread', 'Strangle', 'RatioCallSpread', 'RatioPutSpread']:
            ax.set_title('期权类型:{0:s}，标的:{1:s}，期权费:{2:,.0f}，低执行价:{3:,.2f}，高执行价:{4:,.2f}'.format(self.option_name, self.stock_index_code, self.option_fee, self.strike_price_low, self.strike_price_high), fontsize = 10)
        elif self.option_class in ['ButterflyCallSpread', 'ButterflyPutSpread']:
            ax.set_title('期权类型:{0:s}，标的:{1:s}，期权费:{2:,.0f}，K1:{3:,.2f}，K2:{4:,.2f}，K3:{5:,.2f}'.format(self.option_name, self.stock_index_code, self.option_fee, self.strike_price_low, self.strike_price_mid, self.strike_price_high), fontsize = 10)
        elif self.option_class in ['CalendarCallSpread', 'CalendarPutSpread']:
            ax.set_title('期权类型:{0:s}，标的:{1:s}，期权费:{2:,.0f}，K:{3:,.2f}，到期日1:{4:s},到期日2:{5:s}'.format(self.option_name, self.stock_index_code, self.option_fee, self.strike_price, str(self.end_date), str(self.end_date_after)), fontsize = 10)
        ax.legend()
        fig.savefig('../03_img/{0:s}收益分解.jpg'.format(self.option_name))

    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig, ax