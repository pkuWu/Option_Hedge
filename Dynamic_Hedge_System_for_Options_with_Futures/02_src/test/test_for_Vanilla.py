from classes.options.Vanilla import VanillaCall
from datetime import date


vanilla_call = VanillaCall() # 将类实例化
vanilla_call.set_paras(stock_index_code = '000300.SH',start_date = date(2019,1,2),end_date = date(2019,3,29),K = 3900,r = 0.04,option_fee = 1780800) # 传入参数
vanilla_call.calculate_greeks() # 计算希腊值
greeks_result = vanilla_call.get_greek_df() # 返回希腊值，DataFrame格式