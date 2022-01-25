from classes.strategy.Combinator import Combinator
from classes.options.Option_Contract import Option_Contract
from datetime import date


#设置主连合约、HedgeAll对冲策略
option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
strategy1 = Combinator().get_option(option) # 将类实例化并传入需对冲的期权信息
strategy1.set_month_strategy('Dominant') # 设置月合约策略
strategy1.set_delta_strategy('HedgeAll') # 设置delta对冲敞口维度
# strategy1.set_hedge_strategy('Dominant', 'HedgeAll') # 同时设置月合约和delta敞口维度
strategy1.calculate_future_position() # 计算股指期货position
position = strategy1.get_future_position() # 返回股指期货position
