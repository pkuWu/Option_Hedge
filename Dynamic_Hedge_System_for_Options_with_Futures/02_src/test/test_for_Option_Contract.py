from classes.options.Option_Contract import Option_Contract
from datetime import date

option = Option_Contract() # 将类实例化
option.create_option_portfolio(option_class = 'VanillaCall',option_position = 1, multiplier = 100, start_date = date(2019,1,2),end_date = date(2019,12,31), K=3900, r = 0.04,option_fee = 1780800, stock_index_code = '000300.SH') # 传入参数
greeks = option.get_greek_df() # 返回期权组合的希腊值，DataFrame格式