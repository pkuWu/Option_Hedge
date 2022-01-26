from classes.strategy.Delta_Strategy import *
from classes.options.Option_Contract import Option_Contract
from datetime import date

option = Option_Contract().create_option_portfolio(option_class='VanillaCall', option_position=1,
                                                   option_paras={'stock_index_code': '000300.SH', 'start_date': date(2019, 1, 2),
                                                    'end_date': date(2019, 3, 29), 'K': 3000, 'r': 0.04,
                                                    'option_fee': 1780800})


#ZAKA
zakahedge = Zakamouline().get_option_info(option)
zaka_hedge_df = zakahedge.calculate_target_delta_interval()
target_delta = zakahedge.calculate_target_delta()
#WW
wwhedge = WW_Hedge().get_option_info(option)
ww_hedge_df = wwhedge.calculate_target_delta_interval()

#HedgeAll
hedgeall = HedgeAll().get_option_info(option) # 将策略类实例化并传入参数
hedgeall_target_delta = hedgeall.calculate_target_delta() # 计算需要对冲的cash_delta

#HedgeHalf
hedgehalf = HedgeHalf().get_option_info(option) # 将策略类实例化并传入参数
hedgehalf_target_delta = hedgehalf.calculate_target_delta() # 计算需要对冲的cash_delta