from classes.options.Option_Contract import Option_Contract
from datetime import date
from classes.strategy.Month_Strategy import *


'''
Month_Strategy包括：
    Dominant 主连合约
    Current_Month 当月合约
    Next_Month 下月合约
    Current_Season 当季合约
    Next_Season 下季合约
    Holding_Weighted 持仓量加权
    Volume_Weighted 成交量加权
'''
#Dominant
option = Option_Contract().create_option_portfolio(option_class='VanillaCall', option_position=1, option_paras={'stock_index_code': '000300.SH', 'start_date': date(2019, 1, 2),'end_date': date(2019, 3, 29), 'K': 3000, 'r': 0.04, 'option_fee': 1780800}) # 实例化且传入参数
dominant_strategy = Dominant().get_option_info(option.stock_index_code, option.trade_dates) # 将类实例化并传入参数
dominant_strategy.calculate_future_weight() # 计算权重
dominant_weight = dominant_strategy.get_future_weight() # 返回权重，DataFrame格式

#Holding_Weighted
option = Option_Contract().create_option_portfolio(option_class='VanillaCall', option_position=1, option_paras={'stock_index_code': '000300.SH', 'start_date': date(2019, 1, 2),'end_date': date(2019, 3, 29), 'K': 3000, 'r': 0.04, 'option_fee': 1780800}) # 实例化且传入参数
holding_weighted = Holding_Weighted().get_option_info(option.stock_index_code, option.trade_dates) # 将类实例化并传入参数
holding_weighted.calculate_future_weight() # 计算权重
holding_weighted_weight = holding_weighted.get_future_weight() # 返回权重，DataFrame格式