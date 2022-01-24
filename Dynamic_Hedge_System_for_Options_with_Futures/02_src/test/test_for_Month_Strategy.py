from classes.options.Option_Contract import Option_Contract
from datetime import date
from classes.strategy.Month_Strategy import *


#Dominant
option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
dominant_strategy = Dominant().get_option_info(option) # 将类实例化并传入参数
dominant_strategy.calculate_future_weight() # 计算权重
dominant_weight = dominant_strategy.get_future_weight() # 返回权重，DataFrame格式

#Holding_Weighted
option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
holding_weighted = Holding_Weighted().get_option_info(option) # 将类实例化并传入参数
holding_weighted.calculate_future_weight() # 计算权重
holding_weighted_weight = holding_weighted.get_future_weight() # 返回权重，DataFrame格式
