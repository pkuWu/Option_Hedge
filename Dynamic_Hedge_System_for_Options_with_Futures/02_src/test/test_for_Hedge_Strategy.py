from classes.strategy.Hedge_Strategy import *
from classes.options.Option_Contract import Option_Contract
from datetime import date

option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
HedgeStrategy1 = HedgeAll(option)
target_delta1 = HedgeStrategy1.get_target_delta()


HedgeStrategy2 = HedgeHalf(option)
target_delta2 = HedgeStrategy2.calculate_target_delta()
