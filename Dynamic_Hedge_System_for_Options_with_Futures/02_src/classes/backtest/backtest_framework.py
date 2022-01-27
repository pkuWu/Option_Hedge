from classes.options.Option_Contract import Option_Contract
from classes.strategy.Combinator import Combinator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class BacktestFramework:
    def __init__(self):
        self.reset()

    def reset(self):
        self.option_obj = Option_Contract()
        self.month_strategy = None
        self.delta_strategy = None
        self.strategy_obj = Combinator()
        self.future_position = None
        self.future_code = None
        self.sparse_matrix = None
        self.MCOLORS = ['indianred', 'sandybrown', 'khaki', 'darkseagreen', 'dodgerblue',
                         'mediumpurple', 'lightgrey', 'paleturquoise', 'bisque', 'cornflowerblue']
        self.tr = 0.000023
        self.mr = 0.14
        self.ir = 0.02
        self.max_ratio = 1.5
        self.notional = None
        self.index_position = None
        self.total_index_position = None
        self.single_trading_cost = None
        self.total_trading_cost = None
        self.hedging_trading_cost = None
        self.rollover_trading_cost = None

    def set_options_by_paras(self, option_class, option_position, **option_paras):
        self.option_obj.create_option_portfolio(option_class, option_position, option_paras)
        self.strategy_obj.get_option(self.option_obj.stock_index_code, self.option_obj.trade_dates, self.option_obj.portfolio_position, self.option_obj.option_basket, self.option_obj.greek_df, self.option_obj.public_df)

    def set_month_strategy(self, month_strategy):
        self.month_strategy = month_strategy

    def set_delta_strategy(self, delta_strategy):
        self.delta_strategy = delta_strategy

    def set_hedge_strategy(self, month_strategy, delta_strategy):
        self.set_month_strategy(month_strategy)
        self.set_delta_strategy(delta_strategy)

    def run_backtest(self):
        self.strategy_obj.set_hedge_strategy(self.month_strategy, self.delta_strategy)
        self.future_position = self.strategy_obj.get_future_position()

    def set_future_code(self):
        self.future_code = np.unique(self.strategy_obj.future_code_list)

    def to_sparse_matrix(self):
        self.set_future_code()
        self.sparse_matrix = pd.DataFrame(index=self.strategy_obj.trade_dates, columns=self.future_code)
        for code in self.future_code:
            temp = self.future_position[self.strategy_obj.future_code_list==code].sum(axis=1)
            self.sparse_matrix.loc[:, code] = temp
        return self.sparse_matrix

    def visualize_holding(self):
        self.to_sparse_matrix()
        fig, ax1 = self.init_canvas([0.05, 0.08, 0.88, 0.87])
        ax1.stackplot(self.strategy_obj.trade_dates, self.sparse_matrix.T, colors=self.MCOLORS[:len(self.future_code)],
                      labels=self.future_code)
        ax1.set_title('期货持仓量，策略:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        ax2 = ax1.twinx()
        ax2.plot(self.strategy_obj.trade_dates, self.option_obj.public_df.loc[:,'stock_index_price'],
                 label='{0:s}点位（右轴）'.format(self.strategy_obj.stock_index_name), linewidth=0.5, color='black')
        fig.legend(loc='upper right')
        ax1.set_ylabel('期货持仓量/手数')
        ax2.set_ylabel('{0:s}点位'.format(self.strategy_obj.stock_index_name))
        ax1.set_xlabel('样本日')
        #fig.savefig('../03_img/{0:s}+{1:s}-期货持仓与股指点位.jpg'.format(self.month_strategy,self.delta_strategy))

    def get_notional(self):
        self.notional = abs(self.option_obj.portfolio_position * self.option_obj.multiplier *
                            self.option_obj.public_df.loc[:, 'stock_index_price'][0])

    def get_index_position(self):
        self.index_position = round((self.future_position * self.strategy_obj.future_price).div(
            self.option_obj.public_df.loc[:, 'stock_index_price'], axis=0), 0)
        self.total_index_position = self.index_position.sum(axis=1)

    def calculate_trading_cost(self):
        self.get_index_position()
        self.single_trading_cost = abs(self.future_position.diff().fillna(
            0)) * self.strategy_obj.future_price * self.option_obj.multiplier * self.tr
        self.total_trading_cost = self.single_trading_cost.sum(axis=1)
        self.hedging_trading_cost = abs(self.total_index_position.diff().fillna(0)) * self.option_obj.public_df.loc[:,
                                                                                      'stock_index_price'] * self.option_obj.multiplier * self.tr
        self.rollover_trading_cost = self.total_trading_cost - self.hedging_trading_cost

    def calculate_pnl(self):
        self.get_index_position()
        self.single_future_pnl = self.strategy_obj.future_price.diff().fillna(0) * self.future_position.shift(1).fillna(0) * self.option_obj.multiplier
        self.total_future_pnl = self.single_future_pnl.apply(lambda x: x.sum(), axis=1)
        #股指对冲收益
        self.index_pnl = self.total_index_position.shift(1).fillna(0) * \
                         self.option_obj.public_df['stock_index_price'].diff().fillna(0) * self.option_obj.multiplier
        #基差收益
        self.basis_pnl = self.total_future_pnl - self.index_pnl
        #期货对冲端累积收益
        self.cum_total_pnl = self.total_future_pnl.cumsum()
        #对冲端指数累积收益
        self.cum_index_pnl = self.index_pnl.cumsum()
        #基差累积收益
        self.cum_basis_pnl = self.basis_pnl.cumsum()

    def get_option_pnl(self):
        self.greek_df = self.option_obj.greek_df
        self.option_pnl = self.greek_df['option_value'].diff().fillna(0)

    def visualize_analysis(self):
        # 股指与股指期货头寸分析-折线图
        self.get_index_position()
        fig1, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.index_position.index, self.future_position.sum(axis=1), label='股指期货头寸',
                color='black', linewidth=1)
        ax.plot(self.index_position.index, self.total_index_position, label='股指头寸',
                color='indianred', linewidth=1)
        ax.legend()
        ax.set_xlabel('样本日')
        ax.set_ylabel('头寸')
        ax.set_title('股指期货与对应的股指头寸分析，策略:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        #fig1.savefig('../03_img/头寸分析.jpg')

        # 交易成本分析（除以名义本金）-堆叠图
        self.calculate_trading_cost()
        self.get_notional()
        fig3, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        self.x = pd.concat([self.hedging_trading_cost, self.rollover_trading_cost], axis=1)
        ax.stackplot(self.single_trading_cost.index,
                     pd.concat([self.hedging_trading_cost, self.rollover_trading_cost], axis=1).astype(
                         'float').T / self.notional * 10000,
                     colors=[self.MCOLORS[1], self.MCOLORS[3]], labels=['动态对冲交易成本/名义本金', '展仓交易成本/名义本金'])
        ax.legend()
        y_ticks = ax.get_yticks()
        y_ticklabels = [str(round(i, 2)) + 'bp' for i in y_ticks]
        ax.set_yticklabels(y_ticklabels)
        ax.set_xlabel('样本日')
        ax.set_ylabel('交易成本/名义本金')
        ax.set_title('交易成本分析，策略:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        #fig3.savefig('../03_img/交易成本-名义本金分析.jpg')

        #期货对冲端收益拆解
        self.calculate_pnl()
        self.get_option_pnl()
        fig4, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.index_position.index, self.cum_total_pnl/self.notional, label='期货端收益/名义本金',
                color='black', linewidth=2)
        ax.plot(self.index_position.index, self.option_pnl/self.notional, label='期权端收益/名义本金',
                color=self.MCOLORS[0],linewidth=1)
        ax.plot(self.index_position.index, self.cum_index_pnl/self.notional, '--', label='指数收益/名义本金',
                color='gray', linewidth=1)
        ax.plot(self.index_position.index, self.cum_basis_pnl/self.notional, label='基差收益/名义本金',
                color=self.MCOLORS[4], linewidth=1)
        ax.plot(self.index_position.index, self.total_trading_cost/self.notional, ':', label='交易成本/名义本金',
                color=self.MCOLORS[1], linewidth=1)
        ax.legend()
        ax.set_xlabel('样本日')
        ax.set_ylabel('收益/名义本金')
        ax.set_title('总体收益分解，策略:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig4.savefig('../03_img/总体收益分解.jpg')


    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig, ax