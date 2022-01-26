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

    def set_options_by_paras(self, option_class, option_position, **option_paras):
        self.option_obj.create_option_portfolio(option_class, option_position, option_paras)
        self.strategy_obj.get_option(self.option_obj)

    def set_month_strategy(self, month_strategy):
        self.month_strategy = month_strategy

    def set_delta_strategy(self, delta_strategy):
        self.delta_strategy = delta_strategy

    def set_hedge_strategy(self, month_strategy, delta_strategy):
        self.set_month_strategy(month_strategy)
        self.set_delta_strategy(delta_strategy)

    def run_backtest(self):
        self.strategy_obj.set_month_strategy(self.month_strategy)
        self.strategy_obj.set_delta_strategy(self.delta_strategy)
        self.future_position = self.strategy_obj.get_future_position()

    def set_future_code(self):
        self.future_code = np.unique(self.strategy_obj.future_code_list)

    def to_sparse_matrix(self):
        self.set_future_code()
        self.sparse_matrix = pd.DataFrame(index=self.strategy_obj.trade_dates, columns=self.future_code)
        for code in self.future_code:
            temp = self.future_position[self.strategy_obj.future_code_list==code].sum(axis=1)
            self.sparse_matrix.loc[:,code] = temp
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
        fig.savefig('../03_img/{0:s}+{1:s}-期货持仓与股指点位.jpg'.format(self.month_strategy,self.delta_strategy))

    def visualize_analysis(self):
        pass

    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig, ax