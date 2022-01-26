from classes.backtest.backtest_framework import BacktestFramework as BF
from datetime import date


bf = BF()
bf.set_options_by_paras(option_class='VanillaCall',option_position=-100, stock_index_code='000905.SH', start_date=date(2019,1,2),end_date=date(2019,3,29), K=3000, r=0.04,option_fee=1780800)
bf.set_month_strategy(month_strategy='Holding_Weighted') #股指期货在每个时点上，有4个月合约（近月、下月、当季、下季），这里指仅用下季合约进行对冲，注意展期！ month_strategy in {'Next_Season','Volume_Weighted','Holding_Weighted'}
bf.set_delta_strategy('HedgeAll') #每日收盘前，将delta对冲干净
bf.set_hedge_strategy('Holding_Weighted','HedgeAll') #上两句或者可以缩写成，要求三个策略设置函数都进行定义
bf.run_backtest()
bf.visualize_holding()  #持仓（左轴堆积图）与点位（右轴折线图）的可视化
bf.visualize_analysis() #这里可以提前想一下，要画出哪些图片，在01_doc/Proposal_for_Option_Hedge.md里面写好