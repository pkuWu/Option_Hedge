""" 
@Time    : 2022/1/15 11:13
@Author  : Carl
@File    : backtest.py
@Software: PyCharm
"""
import pandas as pd
import matplotlib.pyplot as plt
from ..options.option_portfolio2 import OptionPortfolio as OP
from ..strategy import *

class Backtest:
    def __init__(self):
        self.fee_rate = 0.00005
        self.backtest_columns = ['option_price','option_value','cash_delta','cash_gamma','cash_theta',
                                 'stock_price','stock_position','stock_value','stock_pnl','trading_cost',
                                 'delta_nav', 'nav', 'cash_account','option_pnl','delta_pnl','gamma_pnl',
                                 'theta_pnl','higher_order_pnl','unhedged_pnl','total_nav','trade_dummy']
        self.reset()

    def reset(self):
        self.set_strategy()
        self.op = OP()

    def set_strategy(self, strategy_name=''):
        self.strategy_name = strategy_name
        self.strategy = None if not strategy_name else eval(strategy_name)()

    def set_option_portfolio(self,paras=None):
        if paras is None:
            raise ValueError('There is no para_dict input')
        else:
            self.op.get_option_list(paras)
            self.size = self.op.get_size(paras)
            self.option_fee = paras.get('notional')

    def init_backtest(self,**kwargs):
        self.op.calculate_greeks()
        self.op.calculate_return_decomposition()
        self.strategy.calculate_hedge_position(self.op.greek_df,self.op.basic_paras_df,**kwargs)
        self.df_backtest = pd.DataFrame(data=None,index=self.op.greek_df.index,columns=self.backtest_columns)

    def run_backtest(self,**kwargs):
        self.init_backtest(**kwargs)
        self.df_backtest.loc[:,['option_price','option_value','cash_delta','cash_gamma','cash_theta']] \
            = self.op.greek_df.loc[:,['option_price','option_value','cash_delta','cash_gamma','cash_theta']]
        self.df_backtest.loc[:,'stock_price'] = self.op.basic_paras_df.loc[:,'stock_price']
        self.df_backtest.loc[:,'stock_position'] = self.strategy.df_hedge.loc[:,'position']
        self.df_backtest.loc[:,'stock_value'] = self.df_backtest.loc[:,'stock_price']*self.df_backtest.loc[:,'stock_position']
        self.df_backtest.loc[:,'stock_pnl'] = self.df_backtest.loc[:,'stock_value'].diff().fillna(0)
        self.df_backtest.loc[:,'trading_cost'] = self.df_backtest.loc[:,'stock_position'].diff().fillna(0).abs()*self.df_backtest.loc[:,'stock_price']*self.fee_rate
        self.df_backtest.loc[:,'delta_nav'] = self.df_backtest.loc[:,'stock_pnl'] - self.df_backtest.loc[:,'trading_cost']
        self.df_backtest.loc[:,'nav'] = self.df_backtest.loc[:,'delta_nav'].cumsum()
        self.df_backtest.loc[:,'cash_account'] = self.option_fee + self.df_backtest.loc[:,'nav'] - self.df_backtest.loc[:,'stock_value']
        self.df_backtest.loc[:,['option_pnl','delta_pnl','gamma_pnl','theta_pnl','higher_order_pnl']] \
            = self.op.decompose_df.loc[:,['option_pnl','delta_pnl','gamma_pnl','theta_pnl','higher_order_pnl']]
        self.df_backtest.loc[:,'unhedged_pnl'] = self.df_backtest.loc[:,'stock_pnl'] + self.df_backtest.loc[:,'delta_pnl']
        self.df_backtest.loc[:,'total_nav'] = self.df_backtest.loc[:,'cash_account'] + self.df_backtest.loc[:,'option_value'] + self.df_backtest.loc[:,'stock_value']
        self.df_backtest.loc[:,'trade_dummy'] = 1
        self.df_backtest.loc[self.df_backtest.loc[:,'stock_position'].diff()==0,'trade_dummy'] = 0
        self.df_backtest = self.df_backtest.astype(float)
        self.df_backtest = self.df_backtest.round(2)
        self.df_backtest.loc[:,'trade_dummy'] = self.df_backtest.loc[:,'trade_dummy'].astype(int)

    def plot_analysis(self):
        # 1.对冲收益分析
        df_plot1 = self.df_backtest.loc[:,['stock_value','option_value','cash_account','total_nav','stock_position','trade_dummy']].copy()
        figure1, ax1 = plt.subplots(figsize=(15,10))
        self.trade_dates = pd.to_datetime(self.df_backtest.index.values)
        ax1.plot(self.trade_dates,df_plot1.loc[:,'stock_value']+df_plot1.loc[:,'cash_account'],linewidth=0.5,color='blue',label='hedge_value')
        ax1.plot(self.trade_dates, df_plot1.loc[:, 'option_value'], linewidth=0.5,color='orange', label='option_value')
        ax1.plot(self.trade_dates, df_plot1.loc[:, 'total_nav'], linewidth=0.5, color='red', label='total_value')
        ax1.set_xlabel('date')
        ax1.set_ylabel('value')
        ax1.legend(loc='upper left')
        ax2 = ax1.twinx()
        ax2.plot(self.trade_dates,df_plot1.loc[:,'stock_position'],linewidth=0.5,color='green',label='stock_position')
        ax2.set_ylabel('position')
        ax2.legend(loc='upper right')
        plt.show()

