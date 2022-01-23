from classes.options.Option_Contract import Option_Contract
from datetime import date

#看涨期权
option = Option_Contract().create_option_portfolio(option_class='VanillaCall',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks = option.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
option.calculate_portfolio_pnl_df() # 计算收益分解
pnl = option.get_pnl_df() # 返回收益分解
option.visualize_pnl() # 收益分解可视化，存储在03_img

#牛市看涨差价
bull_call = Option_Contract().create_option_portfolio(option_class='BullCallSpread',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K_low=3000, K_high=3200, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_bull_call = bull_call.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
bull_call.calculate_portfolio_pnl_df() # 计算收益分解
pnl_bull_call = bull_call.get_pnl_df() # 返回收益分解
bull_call.visualize_pnl() # 收益分解可视化，存储在03_img

#盒式差价
box = Option_Contract().create_option_portfolio(option_class='BoxSpread',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K_low=3000, K_high=3200, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_box = box.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
box.calculate_portfolio_pnl_df() # 计算收益分解
pnl_box = box.get_pnl_df() # 返回收益分解
box.visualize_pnl() # 收益分解可视化，存储在03_img

#跨式组合
straddle = Option_Contract().create_option_portfolio(option_class='Straddle',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_straddle = straddle.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
straddle.calculate_portfolio_pnl_df() # 计算收益分解
pnl_straddle = straddle.get_pnl_df() # 返回收益分解
straddle.visualize_pnl() # 收益分解可视化，存储在03_img

#宽跨式组合
strangle = Option_Contract().create_option_portfolio(option_class='Strangle',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K_low=3000, K_high=3200, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_strangle = strangle.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
strangle.calculate_portfolio_pnl_df() # 计算收益分解
pnl_strangle = strangle.get_pnl_df() # 返回收益分解
strangle.visualize_pnl() # 收益分解可视化，存储在03_img

#蝶式差价
butterfly_call = Option_Contract().create_option_portfolio(option_class='ButterflyCallSpread',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K_low=3000, K_mid=3100, K_high=3200, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_butterfly_call = butterfly_call.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
butterfly_call.calculate_portfolio_pnl_df() # 计算收益分解
pnl_butterfly_call = butterfly_call.get_pnl_df() # 返回收益分解
butterfly_call.visualize_pnl() # 收益分解可视化，存储在03_img

#日历差价
calendar_call = Option_Contract().create_option_portfolio(option_class='CalendarCallSpread',option_position=1, stock_index_code='000300.SH', start_date=date(2019,1,2),end_date_before=date(2019,3,29), end_date_after=date(2019,6,28), K=3300, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_calendar_call = calendar_call.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
calendar_call.calculate_portfolio_pnl_df() # 计算收益分解
pnl_calendar_call = calendar_call.get_pnl_df() # 返回收益分解
calendar_call.visualize_pnl() # 收益分解可视化，存储在03_img

#看涨比率差价多头（Option_Contract里写的是空头，这里position传负数即可）
ratio_call = Option_Contract().create_option_portfolio(option_class='RatioCallSpread',option_position=(-10), stock_index_code='000300.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K_low=3000, K_high=3300, r=0.04,option_fee=1780800) # 实例化且传入参数
greeks_ratio_call = ratio_call.get_greek_df() # 返回期权组合的希腊值，DataFrame格式
ratio_call.calculate_portfolio_pnl_df() # 计算收益分解
pnl_ratio_call = ratio_call.get_pnl_df() # 返回收益分解
ratio_call.visualize_pnl() # 收益分解可视化，存储在03_img
