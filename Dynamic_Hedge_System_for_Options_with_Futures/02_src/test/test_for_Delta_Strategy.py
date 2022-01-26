from classes.strategy.Delta_Strategy import *
from classes.options.Option_Contract import Option_Contract
from datetime import date


'''
Delta_Strategy包括：
    HedgeAll 全部对冲
    HedgeHalf 对冲一半
    WW_Hedge 用WW策略对冲
    Zakamouline 用Zakamouline策略对冲
'''
option = Option_Contract().create_option_portfolio(option_class='VanillaCall', option_position=1,
                                                   option_paras={'stock_index_code': '000300.SH', 'start_date': date(2019, 1, 2),
                                                    'end_date': date(2019, 3, 29), 'K': 3000, 'r': 0.04,
                                                    'option_fee': 1780800})

#HedgeAll
hedgeall = HedgeAll().get_option_info(option) # 将策略类实例化并传入参数
hedgeall.calculate_target_delta() # 计算需要对冲的cash_delta
hedgeall_target_delta = hedgeall.get_target_delta() # 返回需要对冲的cash_delta

#HedgeHalf
hedgehalf = HedgeHalf().get_option_info(option) # 将策略类实例化并传入参数
hedgehalf.calculate_target_delta() # 计算需要对冲的cash_delta
hedgehalf_target_delta = hedgehalf.get_target_delta()# 返回需要对冲的cash_delta

#Zakamouline
zakahedge = Zakamouline().get_option_info(option)
zakahedge.calculate_target_delta()
zakahedge_target_delta = zakahedge.get_target_delta()

#WW_Hedge
wwhedge = WW_Hedge().get_option_info(option)
wwhedge.calculate_target_delta()
wwhedge_target_delta = wwhedge.get_target_delta()