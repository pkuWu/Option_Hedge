from classes.options.Option_Contract import OptionContract
from datetime import date

option = OptionContract() # 将类实例化
option.create_option_portfolio(option_class = 'VanillaCall',option_position = 1, notional = 12e6, start_date = date(2019,1,2),end_date = date(2019,12,31), K=3900, r = 0.04,option_fee = 1780800, stock_index_code = '000300.SH', start_price = 2969.5353) # 传入参数
greeks = option.get_greeks() # 返回期权组合的希腊值，DataFrame格式
