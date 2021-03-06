from classes.options.Option_Contract import Option_Contract
from classes.strategy.Combinator import Combinator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_pdf import PdfPages
import re
from .reportTemplate import ReportTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, ListItem, ListFlowable

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
            temp = self.future_position[self.strategy_obj.future_code_list == code].sum(axis=1)
            self.sparse_matrix.loc[:, code] = temp
        return self.sparse_matrix

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
        #self.get_index_position()
        self.get_option_pnl()
        self.single_future_pnl = self.strategy_obj.future_price.diff().fillna(0) * self.future_position.shift(1).fillna(0) * self.option_obj.multiplier
        self.total_future_pnl = self.single_future_pnl.apply(lambda x: x.sum(), axis=1)
        #??????????????????
        self.index_pnl = self.total_index_position.shift(1).fillna(0) * \
                         self.option_obj.public_df['stock_index_price'].diff().fillna(0) * self.option_obj.multiplier
        #????????????
        self.basis_pnl = self.total_future_pnl - self.index_pnl
        #???????????????????????????
        self.cum_future_pnl = self.total_future_pnl.cumsum()
        #???????????????????????????
        self.cum_index_pnl = self.index_pnl.cumsum()
        #??????????????????
        self.cum_basis_pnl = self.basis_pnl.cumsum()

    def calculate_total_pnl(self):
        self.calculate_account_info()
        #????????????
        self.total_pnl = self.total_future_pnl + self.option_pnl - self.total_trading_cost - self.account_info['interest_fee']

    def get_option_pnl(self):
        self.option_pnl = self.option_obj.pnl_df.loc[:, 'option_pnl']

    def calculate_account_info(self):
        self.calculate_pnl()
        future_value = (self.future_position * self.strategy_obj.future_price).sum(axis=1) * self.strategy_obj.multiplier
        self.account_info = pd.DataFrame(index=self.strategy_obj.trade_dates,
                                         columns=['margin_account', 'interest_fee', 'delta_nav', 'nav', 'cash_account'])
        self.account_info.loc[self.account_info.index[0], 'margin_account'] = abs(future_value[0]) * self.mr
        for i in range(1, len(self.account_info)):
            self.account_info.loc[self.account_info.index[i], 'margin_account'] = min(max(abs(future_value[i]) * self.mr,
                                                                                          self.account_info.loc[self.account_info.index[i-1], 'margin_account'] + self.total_future_pnl[i] - \
                                                                                          self.total_trading_cost[i]),
                                                                                      abs(future_value[i]) * self.mr * self.max_ratio)
        self.account_info.loc[self.account_info.index[0], 'interest_fee'] = 0
        for i in range(len(self.account_info)):
            self.account_info.loc[self.account_info.index[i], 'delta_nav'] = self.total_future_pnl[i] - self.total_trading_cost[i] - self.account_info.loc[self.account_info.index[i], 'interest_fee']
            self.account_info.loc[self.account_info.index[i], 'nav'] = self.account_info.loc[:, 'delta_nav'].cumsum()[i]
            self.account_info.loc[self.account_info.index[i], 'cash_account'] = self.account_info.loc[self.account_info.index[i], 'nav'] - self.account_info.loc[self.account_info.index[i], 'margin_account']
            if i < len(self.account_info)-1:
                self.account_info.loc[self.account_info.index[i+1], 'interest_fee'] = -self.account_info.loc[self.account_info.index[i], 'cash_account'] * self.ir / 365

    def visualize_analysis(self, report=True):
        # ??????????????????
        self.to_sparse_matrix()
        fig1, ax1 = self.init_canvas([0.05, 0.08, 0.88, 0.87])
        ax1.stackplot(self.strategy_obj.trade_dates, self.sparse_matrix.T, colors=self.MCOLORS[:len(self.future_code)],
                      labels=self.future_code)
        ax1.set_title('????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        ax2 = ax1.twinx()
        ax2.plot(self.strategy_obj.trade_dates, self.option_obj.public_df.loc[:, 'stock_index_price'],
                 label='{0:s}??????????????????'.format(self.strategy_obj.stock_index_name), linewidth=0.5, color='black')
        fig1.legend(loc='upper right')
        ax1.set_ylabel('???????????????/??????')
        ax2.set_ylabel('{0:s}??????'.format(self.strategy_obj.stock_index_name))
        ax1.set_xlabel('?????????')
        fig1.savefig('../03_img/???????????????????????????.jpg')

        # ?????????????????????????????????-?????????
        self.get_index_position()
        fig2, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.index_position.index, self.future_position.sum(axis=1), label='??????????????????',
                color='black', linewidth=1)
        ax.plot(self.index_position.index, self.total_index_position, label='????????????',
                color='indianred', linewidth=1)
        ax.legend()
        ax.set_xlabel('?????????')
        ax.set_ylabel('??????')
        ax.set_title('???????????????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig2.savefig('../03_img/????????????.jpg')

        # ??????????????????????????????????????????-?????????
        self.calculate_trading_cost()
        self.get_notional()
        fig3, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        self.x = pd.concat([self.hedging_trading_cost, self.rollover_trading_cost], axis=1)
        ax.stackplot(self.single_trading_cost.index,
                     pd.concat([self.hedging_trading_cost, self.rollover_trading_cost], axis=1).astype(
                         'float').T / self.notional * 10000,
                     colors=[self.MCOLORS[1], self.MCOLORS[3]], labels=['????????????????????????/????????????', '??????????????????/????????????'])
        ax.legend()
        y_ticks = ax.get_yticks()
        y_ticklabels = [str(round(i, 2)) + 'bp' for i in y_ticks]
        ax.yaxis.set_major_locator(mticker.FixedLocator(y_ticks))
        ax.set_yticklabels(y_ticklabels)
        ax.set_xlabel('?????????')
        ax.set_ylabel('????????????/????????????')
        ax.set_title('???????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig3.savefig('../03_img/????????????-??????????????????.jpg')

        # ??????????????????
        self.option_obj.calculate_portfolio_pnl_df()
        self.calculate_total_pnl()
        fig4, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.index_position.index,self.total_pnl.cumsum()/self.notional,label='????????????/????????????',
                color='black', linewidth=2)
        ax.plot(self.index_position.index, self.cum_future_pnl/self.notional, label='???????????????/????????????',
                color=self.MCOLORS[5], linewidth=1)
        ax.plot(self.index_position.index, self.option_pnl.cumsum()/self.notional, label='???????????????/????????????',
                color=self.MCOLORS[0],linewidth=1)
        ax.plot(self.index_position.index, self.total_trading_cost.cumsum()/self.notional, ':', label='??????????????????/????????????',
                color=self.MCOLORS[1], linewidth=1)
        ax.plot(self.index_position.index, self.account_info['interest_fee'].cumsum()/self.notional, ':', label='????????????????????????/????????????',
                color=self.MCOLORS[4], linewidth=1)
        ax.legend()
        ax.set_xlabel('?????????')
        ax.set_ylabel('??????/????????????')
        ax.set_title('???????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig4.savefig('../03_img/??????????????????.jpg')

        #?????????????????????
        fig15, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.index_position.index, self.cum_future_pnl/self.notional, label='???????????????/????????????',
                color=self.MCOLORS[5], linewidth=1)
        ax.plot(self.index_position.index, self.cum_index_pnl/self.notional, '--', label='????????????/????????????',
                color='gray', linewidth=1)
        ax.plot(self.index_position.index, self.cum_basis_pnl/self.notional, label='????????????/????????????',
                color=self.MCOLORS[4], linewidth=1)
        ax.legend()
        ax.set_xlabel('?????????')
        ax.set_ylabel('??????/????????????')
        ax.set_title('??????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig15.savefig('../03_img/?????????????????????.jpg')

        # ??????????????????
        fig0, ax = self.init_canvas([0.05, 0.08, 0.88, 0.87])
        ax.plot(self.option_obj.trade_dates, self.option_obj.pnl_df.loc[:, 'delta_pnl'].cumsum() + self.cum_future_pnl,
                label='adj_delta_pnl')
        ax.plot(self.option_obj.trade_dates, self.option_obj.pnl_df.loc[:, 'gamma_pnl'].cumsum(), label='gamma_pnl')
        ax.plot(self.option_obj.trade_dates, self.option_obj.pnl_df.loc[:, 'vega_pnl'].cumsum(), label='vega_pnl')
        ax.plot(self.option_obj.trade_dates, self.option_obj.pnl_df.loc[:, 'theta_pnl'].cumsum(), label='theta_pnl')
        ax.plot(self.option_obj.trade_dates, self.option_obj.pnl_df.loc[:, 'option_pnl'].cumsum() + self.cum_future_pnl,
                label='adj_option_pnl')
        ax.plot(self.option_obj.trade_dates, self.option_obj.pnl_df.loc[:, 'high_order_pnl'].cumsum(),
                label='high_order_pnl')
        ax.legend()
        ax.set_xlabel('?????????')
        ax.set_ylabel('??????')
        ax.set_title('???????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig0.savefig('../03_img/??????????????????.jpg')

        # ???????????????/?????????????????????????????????
        fig5, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.cum_future_pnl/self.notional, bins=40, edgecolor='k', color=self.MCOLORS[0])
        ax.set_xlabel('???????????????/????????????')
        ax.set_ylabel('??????')
        ax.set_title('???????????????/??????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig5.savefig('../03_img/???????????????-????????????.jpg')

        # ???????????????/?????????????????????????????????
        fig6, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.option_pnl/self.notional, bins=40, edgecolor='k', color=self.MCOLORS[3])
        ax.set_xlabel('???????????????/????????????')
        ax.set_ylabel('??????')
        ax.set_title('???????????????/??????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig6.savefig('../03_img/???????????????-????????????.jpg')

        # ????????????/?????????????????????????????????
        fig7, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.cum_index_pnl/self.notional, bins=40, edgecolor='k', color=self.MCOLORS[1])
        ax.set_xlabel('????????????/????????????')
        ax.set_ylabel('??????')
        ax.set_title('????????????/??????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig7.savefig('../03_img/????????????-????????????.jpg')

        # ????????????/?????????????????????????????????
        fig8, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.cum_basis_pnl/self.notional, bins=40, edgecolor='k', color=self.MCOLORS[2])
        ax.set_xlabel('????????????/????????????')
        ax.set_ylabel('??????')
        ax.set_title('????????????/??????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig8.savefig('../03_img/????????????-????????????.jpg')

        # ????????????/?????????????????????????????????
        fig9, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.total_trading_cost/self.notional, bins=40, edgecolor='k', color=self.MCOLORS[4])
        ax.set_xlabel('????????????/????????????')
        ax.set_ylabel('??????')
        ax.set_title('????????????/??????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig9.savefig('../03_img/????????????-????????????.jpg')

        #??????????????????????????????????????????????????????-?????????
        fig10, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.account_info.index, self.account_info.loc[:, 'margin_account'], label='???????????????',
                color='black', linewidth=1)
        ax.plot(self.account_info.index, self.account_info.loc[:, 'cash_account'], label='????????????',
                color='indianred', linewidth=1)
        ax.legend()
        ax.set_xlabel('?????????')
        ax.set_ylabel('????????????')
        ax.set_title('?????????????????????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig10.savefig('../03_img/????????????????????????????????????????????????.jpg')

        # ??????????????????????????????????????????
        fig11, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.account_info.loc[:, 'margin_account'], bins=40, edgecolor='k', color=self.MCOLORS[5])
        ax.set_xlabel('???????????????????????????')
        ax.set_ylabel('??????')
        ax.set_title('???????????????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig11.savefig('../03_img/???????????????.jpg')

        # ?????????????????????????????????
        fig12, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.account_info.loc[:, 'cash_account'], bins=40, edgecolor='k', color=self.MCOLORS[6])
        ax.set_xlabel('????????????????????????')
        ax.set_ylabel('??????')
        ax.set_title('????????????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig12.savefig('../03_img/????????????.jpg')

        # ??????????????????????????????/????????????-?????????
        fig13, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.account_info.index, self.account_info.loc[:, 'interest_fee']/self.notional, label='??????????????????????????????/????????????',
                color='black', linewidth=1)
        ax.legend()
        ax.set_xlabel('?????????')
        ax.set_ylabel('??????????????????????????????/????????????')
        ax.set_title('?????????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig13.savefig('../03_img/????????????????????????????????????.jpg')

        # ??????????????????????????????/?????????????????????????????????
        fig14, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.hist(self.account_info.loc[:, 'interest_fee']/self.notional, bins=40, edgecolor='k', color=[self.MCOLORS[7]])
        ax.set_xlabel('??????????????????????????????/????????????')
        ax.set_ylabel('??????')
        ax.set_title('??????????????????????????????/??????????????????????????????????????????:{0:s}+{1:s}'.format(self.month_strategy, self.delta_strategy))
        fig14.savefig('../03_img/??????????????????????????????-?????????????????????????????????.jpg')

    def generate_report(self):
        self.visualize_analysis()

        rt = ReportTemplate()
        story = list()
        # story.append(Paragraph('<para><b>??????????????????</b></para>', style=rt.txt_style['??????1']))
        story.append(Paragraph('????????????????????????-????????????', style=rt.txt_style['??????1']))
        story.append(Spacer(240, 20))

        story.append(Paragraph('1.????????????', style=rt.txt_style['??????2']))
        story.append(Spacer(240, 10))
        table_data1 = [
            ['????????????', '????????????'],
            ['????????????', self.option_obj.option_class],
            ['????????????', self.option_obj.portfolio_position],
            ['????????????', self.notional],
            ['????????????', self.option_obj.start_date],
            ['????????????', self.option_obj.end_date],
            ['????????????', self.option_obj.stock_index_code],
            ['????????????', self.option_obj.strike_price],
            ['Delta Strategy', self.delta_strategy],
            ['Month Strategy', self.month_strategy]
        ]
        story.append(rt.gen_table(table_data1))
        story.append(Spacer(240, 10))

        story.append(Paragraph('2.??????????????????', style=rt.txt_style['??????2']))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/??????????????????.jpg'))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.????????????', style=rt.txt_style['??????2']))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.1 ???????????????', style=rt.txt_style['??????3']))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/???????????????????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????.jpg'))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.2 ??????????????????', style=rt.txt_style['??????3']))
        story.append(Spacer(240, 10))
        table_data2 = [
            ['?????????', '???????????????', '???????????????', '????????????', '????????????', '????????????'],
            [self.total_pnl.sum().round(2), self.cum_future_pnl[-1].round(2), self.option_pnl.sum().round(2),
             self.total_trading_cost.sum().round(2), self.account_info['interest_fee'].sum().round(2),
             self.cal_MaxDrawdown(self.total_pnl).round(2)]
        ]
        story.append(rt.gen_table(table_data2))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/??????????????????.jpg'))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.3 ?????????????????????', style=rt.txt_style['??????3']))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/?????????????????????.jpg'))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.4 ??????????????????', style=rt.txt_style['??????3']))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????-??????????????????.jpg'))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.5 ??????????????????????????????', style=rt.txt_style['??????3']))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????????????????????????????????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????????????????????????????.jpg'))
        story.append(Spacer(240, 10))

        story.append(Paragraph('3.6 ?????????????????????', style=rt.txt_style['??????3']))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/???????????????-????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????-????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????-????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/???????????????-????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????-????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/???????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/????????????.jpg'))
        story.append(Spacer(240, 10))
        story.append(rt.gen_img('../03_img/??????????????????????????????-?????????????????????????????????.jpg'))

        report_name = '../02_src/report/???????????????{0:s}+{1:s}??????????????????{2:s}+{3:s}.pdf'.format(
            self.strategy_obj.stock_index_name, self.option_obj.option_name, self.month_strategy, self.delta_strategy)
        doc = SimpleDocTemplate(report_name)
        doc.build(story)

    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig, ax

    @staticmethod
    def cal_MaxDrawdown(series):
        return np.max(series.cummax() - series)
