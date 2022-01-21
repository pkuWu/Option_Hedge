from classes.options.Vanilla import VanillaCall
from datetime import date


vanilla = VanillaCall() # 将类实例化
vanilla.set_paras(multiplier = 100,start_date = date(2019,1,2),end_date = date(2019,12,31),K=3900,r = 0.04,option_fee = 1780800,stock_index_code = '000300.SH') # 传入参数
vanilla.calculate_greeks() # 计算希腊值
greeks_result = vanilla.get_greek_df() # 返回计算结果，DataFrame格式