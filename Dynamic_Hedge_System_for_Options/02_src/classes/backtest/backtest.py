""" 
@Time    : 2022/1/15 11:13
@Author  : Carl
@File    : backtest.py
@Software: PyCharm
"""
import pandas as pd
from ..backtest.backtestFramework import BacktestFramework

class Backtest(BacktestFramework):
    def __init__(self):
        super(Backtest, self).__init__()
        self.fee_rate = 0.00005

    def run_backtest(self, df_pos):
        self.df_backtest = df_pos.copy(deep=True)
        self.df_backtest.loc[:, 'pnl'] = -self.df_backtest['stock_price']*self.df_backtest['position'].diff()
        self.df_backtest.loc[:, 'fee'] = self.df_backtest['pnl'].abs() * self.fee_rate
        self.df_backtest.loc[:, 'cash'] = self.df_backtest['stock_price'] * self.df_backtest['position'] + \
                                          self.df_backtest['pnl'].cumsum() - self.df_backtest['fee'].cumsum()

    def summary(self):
        return self.df_backtest.loc[:, ['pnl', 'fee', 'cash']].sum()
