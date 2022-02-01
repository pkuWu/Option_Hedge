""" 
@Time    : 2022/1/15 11:13
@Author  : Carl
@File    : backtest.py
@Software: PyCharm
"""
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk
from ..options.option_portfolio2 import OptionPortfolio as OP
from ..strategy import *

class Backtest:
    def __init__(self):
        self.fee_rate = 0.00005
        self.r = 0.04

    def set_paras_by_dict(self, para_dict=None):
        if para_dict is not None:
            self.paras = para_dict.copy()
        else:
            raise ValueError('Paras cannot be empty!!!')

    def set_strategy(self, strategy_name=None):
        try:
            self.strategy = eval(strategy_name)()
        except:
            raise ValueError('Invalid strategy name!!!')
        self.set_option_portfolio()
        self.strategy.calculate_hedge_position(self.op.get_greek_df(), self.op.get_basic_paras_df(),
                                               r=self.r, K=self.paras.get('K'), size=self.size)

    def set_option_portfolio(self):
        self.op = OP()
        self.op.get_option_list(self.paras)
        self.size = self.op.get_size(self.paras)
        self.option_fee = self.paras.get('notional')

    def run_backtest(self):
        self.df_backtest = self.op.get_greek_df().loc[:, ['option_price', 'option_value', 'cash_delta', 'cash_gamma', 'cash_theta']].copy()
        self.df_backtest.loc[:, ['option_pnl', 'delta_pnl', 'theta_pnl', 'gamma_pnl', 'vega_pnl', 'higher_order_pnl']] = \
            self.op.get_return_decomposition().loc[:, ['option_pnl', 'delta_pnl', 'theta_pnl', 'gamma_pnl', 'vega_pnl', 'higher_order_pnl']]
        self.df_backtest.loc[:, 'stock_price'] = self.op.basic_paras_df.loc[:, 'stock_price']
        self.df_backtest.loc[:, 'stock_position'] = self.strategy.df_hedge.loc[:, 'position']
        self.df_backtest.loc[:, 'stock_value'] = self.df_backtest.loc[:, 'stock_price']*self.df_backtest.loc[:, 'stock_position']
        self.df_backtest.loc[:, 'stock_pnl'] = self.df_backtest.loc[:,'stock_value'].diff().fillna(0)
        self.df_backtest.loc[:,'trading_cost'] = self.df_backtest.loc[:, 'stock_position'].diff().fillna(self.df_backtest['stock_value'][0]).abs() * \
                                                 self.df_backtest.loc[:, 'stock_price'] * self.fee_rate
        self.df_backtest.loc[:, 'delta_nav'] = self.df_backtest.loc[:, 'stock_pnl'] - self.df_backtest.loc[:, 'trading_cost']
        self.df_backtest.loc[:, 'nav'] = self.df_backtest.loc[:, 'delta_nav'].cumsum()
        self.df_backtest.loc[:, 'cash_account'] = self.option_fee + self.df_backtest.loc[:, 'nav'] - self.df_backtest.loc[:, 'stock_value']
        self.df_backtest.loc[:,'unhedged_pnl'] = self.df_backtest.loc[:, 'stock_pnl'] + self.df_backtest.loc[:, 'delta_pnl']
        self.df_backtest.loc[:,'total_nav'] = self.df_backtest.loc[:, 'cash_account'] - \
                                              self.df_backtest.loc[:, 'option_value'] + \
                                              self.df_backtest.loc[:, 'stock_value']
        self.df_backtest = self.df_backtest.round(2)
        self.df_backtest.loc[:, 'trade_dummy'] = 1
        self.df_backtest.loc[self.df_backtest.loc[:, 'stock_position'].diff() == 0, 'trade_dummy'] = 0
        self.hedge_pnl_analysis()

    def hedge_pnl_analysis(self):
        self.trade_dates = pd.to_datetime(self.df_backtest.index.values)
        self.hedge_summary()
        self.hedge_pnl_plot()
        self.pnl_decomposition_plot()

    def hedge_summary(self):
        self.hedge_pnl_summary = pd.Series(self.df_backtest.loc[:, ['total_nav', 'stock_pnl']].sum().values, index=['total_pnl', 'stock_pnl'])
        self.hedge_pnl_summary['option_pnl'] = self.option_fee-self.df_backtest.loc[:, 'option_pnl'].sum()
        self.hedge_pnl_summary['trading_cost'] = self.df_backtest.loc[:, 'trading_cost'].sum()
        self.hedge_pnl_summary['min_cash'] = self.df_backtest.loc[:, 'cash_account'].min()
        self.hedge_pnl_summary['max_drawdown'] = self.cal_MDD(self.df_backtest.loc[:, 'total_nav'])
        self.hedge_pnl_summary = self.hedge_pnl_summary.round(2)
        self.decomposition_summary = pd.Series(self.df_backtest.loc[:, ['gamma_pnl', 'vega_pnl', 'theta_pnl', 'higher_order_pnl',
                                        'unhedged_pnl', 'trading_cost', 'total_nav']].sum().values, index=['total_gamma_pnl',
                                        'total_vega_pnl', 'total_theta_pnl', 'total_higher_order_pnl', 'total_unhedged_pnl',
                                        'total_trading_cost', 'total_profit'])
        self.decomposition_summary = self.decomposition_summary.round(decimals=2)

    def hedge_pnl_plot(self):
        df_plot = self.df_backtest.loc[:, ['option_value', 'stock_value', 'cash_account', 'total_nav',
                                           'trade_dummy', 'stock_position']].copy()
        df_plot.loc[:, 'option_value'] = -df_plot.loc[:, 'option_value']
        fig, ax1 = self.init_canvas([0.05, 0.05, 0.78, 0.85])
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'stock_value'] + df_plot.loc[:, 'cash_account'], linewidth=0.5,
                 color='blue', label='hedge_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'option_value'], linewidth=1, color='orange', label='option_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'total_nav'], linewidth=1, color='red', label='total_value')
        for tradeday in pd.to_datetime(df_plot[df_plot['trade_dummy'] == 1].index):
            ax1.axvline(tradeday, linewidth=0.5, color='lightgrey', zorder=0)
        ax1.legend(bbox_to_anchor=(1.025, 0.95), loc='upper left', borderaxespad=1, fontsize=8)
        ax1_lim = [df_plot.values.min(), df_plot.values.max()]
        ax1.set_ylim(ax1_lim[0]-0.1*(ax1_lim[1]-ax1_lim[0]), ax1_lim[1]+(ax1_lim[1]-ax1_lim[0]))
        ax2 = ax1.twinx()
        ax2.plot(self.trade_dates, df_plot.loc[:, 'stock_position'], linewidth=1, color='green', drawstyle='steps-post', label='stock_position(右轴)')
        ax2_lim = [min(df_plot.loc[:, 'stock_position']), max(df_plot.loc[:, 'stock_position'])]
        ax2.set_ylim(2*ax2_lim[0]-ax2_lim[1], ax2_lim[1]*1.1)
        ax2.legend(bbox_to_anchor=(1.005, 1), loc='upper left', borderaxespad=1, fontsize=8)
        strategy_name = re.findall(r'\'(.*?)\'', str(type(self.strategy)))[0].split('.')[-1]
        ax1.set_title('收益情况图-对冲方法：{}-总利润：{}-期权盈利：{}-股票盈利：{}\n交易成本：{}-现金账户最小值：{}-最大回撤：{}'.
                      format(strategy_name, *self.hedge_pnl_summary.values))
        # plt.show()
        fig.savefig('../03_img/股票对冲回测.jpg')

    def pnl_decomposition_plot(self):
        df_plot = self.df_backtest.loc[:, ['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'vega_pnl',
                                           'higher_order_pnl', 'trading_cost']].cumsum()
        df_plot.loc[:, ['position_rate', 'upper_bound', 'lower_bound']] = self.strategy.get_hedge_df().loc[:, ['position_rate', 'up_bound', 'low_bound']].values
        fig, ax1 = self.init_canvas([0.06, 0.07, 0.73, 0.85])
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'option_pnl'], linewidth=0.5, label='total_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'delta_pnl'], linewidth=0.5, label='delta_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'gamma_pnl'], linewidth=0.5, label='gamma_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'theta_pnl'], linewidth=0.5, label='theta_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'vega_pnl'], linewidth=0.5, label='vega_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'higher_order_pnl'], linewidth=0.5, label='higher_order_value')
        ax1.plot(self.trade_dates, df_plot.loc[:, 'trading_cost'], linewidth=0.5, label='trade_cum_cost')
        for tradeday in pd.to_datetime(df_plot[df_plot['position_rate'].diff() != 0].index):
            ax1.axvline(tradeday, linewidth=0.5, color='lightgrey', zorder=0)
        ax1.legend(bbox_to_anchor=(1.03, 0.85), loc='upper left', borderaxespad=1, fontsize=9)
        ax2 = ax1.twinx()
        ax2.plot(self.trade_dates, df_plot.loc[:, 'position_rate'], linewidth=0.5, drawstyle='steps-post', label='asset_delta（右轴）', c='black')
        ax2.plot(self.trade_dates, df_plot.loc[:, 'upper_bound'], linewidth=0.5, label='delta_upper_bound', c='pink')
        ax2.plot(self.trade_dates, df_plot.loc[:, 'lower_bound'], linewidth=0.5, label='delta_lower_bound', c='pink')
        ax2_lim = [np.percentile(df_plot.loc[:, 'lower_bound'], 5), np.percentile(df_plot.loc[:, 'upper_bound'], 95)]
        ax2.set_ylim(2*ax2_lim[0]-ax2_lim[1], ax2_lim[1]*1.1)
        # ax2.set_ylim(-1, 2)
        ax2.legend(bbox_to_anchor=(1.03, 1), loc='upper left', borderaxespad=1, fontsize=9)
        strategy_name = re.findall(r'\'(.*?)\'', str(type(self.strategy)))[0].split('.')[-1]
        ax1.set_title('收益分解图-对冲方法：{}-总利润：{}-gamma：{}-theta：{}\nvega：{}-高阶：{}-未对冲损益：{}-交易成本：{}'.format(
            strategy_name, self.decomposition_summary['total_profit'], self.decomposition_summary['total_gamma_pnl'],
                   self.decomposition_summary['total_theta_pnl'], self.decomposition_summary['total_vega_pnl'],
                   self.decomposition_summary['total_higher_order_pnl'], self.decomposition_summary['total_unhedged_pnl'],
                   self.decomposition_summary['total_trading_cost']))
        # plt.show()
        fig.savefig('../03_img/对冲收益分解.jpg')

    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig, ax

    @staticmethod
    def cal_MDD(series):
        return np.max(series.cummax()-series)


