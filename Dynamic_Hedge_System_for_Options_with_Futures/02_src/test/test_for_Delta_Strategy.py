from classes.strategy.Delta_Strategy import *
from classes.options.Option_Contract import Option_Contract
from datetime import date


#HedgeAll
option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
hedgeall = HedgeAll().get_option_info(option) # 将策略类实例化并传入参数
hedgeall.calculate_target_delta() # 计算需要对冲的cash_delta
hedgeall_target_delta = hedgeall.get_target_delta() # 返回需要对冲的cash_delta

#HedgeHalf
option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
hedgehalf = HedgeHalf().get_option_info(option) # 将策略类实例化并传入参数
hedgehalf.calculate_target_delta() # 计算需要对冲的cash_delta
hedgehalf_target_delta = hedgehalf.get_target_delta()# 返回需要对冲的cash_delta
