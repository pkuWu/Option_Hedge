from classes.options.Option_Contract import Option_Contract
from datetime import date

#看涨期权
option = Option_Contract() # 将类实例化
option.create_option_portfolio(option_class = 'VanillaCall',option_position = 1, stock_index_code = '000300.SH', start_date = date(2019,1,2),end_date = date(2019,3,29), K=3000, r = 0.04,option_fee = 1780800) # 传入参数
greeks = option.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
option.calculate_portfolio_pnl_df() # 计算收益分解
pnl = option.get_pnl_df() # 返回收益分解
# option.visualize_pnl() # 收益分解可视化，存储在03_img

#牛市看涨差价
bull_call = Option_Contract() # 实例化
bull_call.create_option_portfolio(option_class = 'BullCallSpread',option_position = 1, stock_index_code = '000300.SH', start_date = date(2019,1,2),end_date = date(2019,3,29), K_low=3000, K_high = 3200, r = 0.04,option_fee = 1780800) # 传入参数
greeks_bull_call = bull_call.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
bull_call.calculate_portfolio_pnl_df() # 计算收益分解
pnl_bull_call = bull_call.get_pnl_df() # 返回收益分解
# bull_call.visualize_pnl() # 收益分解可视化，存储在03_img
