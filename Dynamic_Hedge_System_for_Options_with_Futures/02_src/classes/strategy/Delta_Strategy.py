from .Delta_StrategyBase import Delta_StrategyBase
import numpy as np
import pandas as pd
from scipy import stats as st
import matplotlib.pyplot as plt


#HEDGE ALL
class HedgeAll(Delta_StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = -self.option_greek_df.loc[:, 'cash_delta']

# HEDGE HALF
class HedgeHalf(Delta_StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = pd.DataFrame(columns=self.option_greek_df.columns)
        self.target_delta[0] = -self.option_greek_df.loc[0, 'cash_delta']
        for i in range(1,len(self.target_delta)):
            #每次对冲增量的一半
            self.target_delta[i] = (self.option_greek_df.loc[i,'cash_delta'] - self.option_greek_df.loc[i-1,'cash_delta'])/2

# Whalley Wilmott method
class WW_Hedge(Delta_StrategyBase):
    def __init__(self,lambda_=0.005,risk_averse=1):
        super().__init__()
        self.risk_averse = risk_averse
        self.lambda_ = lambda_

    def calculate_target_delta_interval(self):
        portfolio_greek_df = self.option_greek_df
        public_df = self.public_df
        self.WW_Hedge_df = pd.DataFrame(0, index=public_df.index, columns=['H0', 'delta', 'delta_upper_bound', 'delta_lower_bound', 'cash_delta', 'cash_delta_up', 'cash_delta_low', 'target_delta'])
        r_list = []
        for i in range(len(self.single_option_info)):
            option_obj = self.single_option_info[i]
            r_list.append(option_obj['r'])
        left_times = self.single_option_info[0]['left_times']
        r = min(r_list)
        self.WW_Hedge_df['H0'] = np.power((3/2*np.exp(r*left_times)*self.lambda_ * public_df['stock_index_price'] * np.power(portfolio_greek_df['gamma'], 2)/self.risk_averse), 1/3)
        self.WW_Hedge_df['delta'] = portfolio_greek_df['delta']
        self.WW_Hedge_df['delta_upper_bound'] = self.WW_Hedge_df['delta']+self.WW_Hedge_df['H0']
        self.WW_Hedge_df['delta_lower_bound'] = self.WW_Hedge_df['delta']-self.WW_Hedge_df['H0']
        self.WW_Hedge_df['cash_delta'] = portfolio_greek_df['cash_delta']
        self.WW_Hedge_df['cash_delta_up'] = self.WW_Hedge_df['delta_upper_bound'] * self.multiplier * public_df['stock_index_price'] * self.portfolio_position
        self.WW_Hedge_df['cash_delta_low'] = self.WW_Hedge_df['delta_lower_bound'] * \
                                             self.multiplier * public_df['stock_index_price'] * \
                                             self.portfolio_position
        return self.WW_Hedge_df

    def calculate_target_delta(self):
        WW_Hedge_df = self.calculate_target_delta_interval()
        WW_Hedge_df.loc[WW_Hedge_df.index[0], 'target_delta'] = self.option_greek_df.loc[self.option_greek_df.index[0],'cash_delta']
        for i in range(1, len(WW_Hedge_df)):
            WW_Hedge_df.loc[WW_Hedge_df.index[i], 'target_delta'] = min(max(WW_Hedge_df.loc[WW_Hedge_df.index[i-1], 'target_delta'], \
                                                                                WW_Hedge_df.loc[WW_Hedge_df.index[i],'cash_delta_low']), \
                                                                            WW_Hedge_df.loc[WW_Hedge_df.index[i],'cash_delta_up'])
        self.target_delta = -WW_Hedge_df['target_delta']

    def visualize_WW(self):
        fig, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.WW_Hedge_df.index, self.WW_Hedge_df['cash_delta'], label='cash_delta', color='sandybrown', linewidth=1)
        ax.plot(self.WW_Hedge_df.index, self.WW_Hedge_df['cash_delta_up'], label='cash_delta_up', color='mediumpurple', linewidth=1)
        ax.plot(self.WW_Hedge_df.index, self.WW_Hedge_df['cash_delta_low'], label='cash_delta_low', color='black', linewidth=1)
        ax.plot(self.WW_Hedge_df.index, self.WW_Hedge_df['target_delta'], label='target_delta', color='indianred', linewidth=2)
        ax.legend()
        ax.set_title('WW策略的delta带与动态调仓', fontsize = 10)
        fig.savefig('../03_img/WW策略的delta带与动态调仓.jpg')

# Zakamouline method
class Zakamouline(Delta_StrategyBase):
    def __init__(self,lambda_=0.005,risk_averse=1):
        super().__init__()
        self.lambda_ = lambda_
        self.risk_averse = risk_averse

    def calculate_target_delta_interval(self):
        portfolio_greek_df = self.option_greek_df
        public_df = self.public_df
        self.Zaka_Hedge_df = pd.DataFrame(0, index=public_df.index, columns=['H0', 'H1', 'adj_delta', 'delta_upper_bound', 'delta_lower_bound', 'adj_cash_delta', 'cash_delta_up', 'cash_delta_low', 'target_delta'])
        r_list = []
        for i in range(len(self.single_option_info)):
            option_obj = self.single_option_info[i]
            option_class = option_obj['option_class']
            greek_df = option_obj['greek_df']
            option_pos = option_obj['option_pos']
            r_list.append(option_obj['r'])
            adj_greek_df = pd.DataFrame(columns=['adj_factor_K','adj_sigma','adj_sigma_T','adj_d1','adj_Nd1','adj_nd1','adj_gamma','adj_delta'])
            adj_greek_df['sigma'] = greek_df['sigma']
            adj_greek_df['adj_factor_K'] = -4.76*np.power(self.lambda_,0.78) / \
                                           np.power(greek_df['left_times'],0.02) \
                                           * np.power(np.exp(-option_obj['r'] * greek_df['left_times']) / adj_greek_df['sigma'], 0.25) * \
                                           np.power(self.risk_averse * greek_df['stock_index_price']**2*np.abs(greek_df['gamma']), 0.15)
            adj_greek_df['adj_sigma'] = adj_greek_df['sigma']*np.sqrt(1+adj_greek_df['adj_factor_K'])
            adj_greek_df['adj_sigma_T'] = adj_greek_df['adj_sigma']*np.sqrt(greek_df['left_times'])
            adj_greek_df['adj_d1'] = (np.log(greek_df['stock_index_price'] / option_obj['K']) + option_obj['r'] * greek_df['left_times']) / adj_greek_df['adj_sigma_T'] + 0.5 * adj_greek_df['adj_sigma_T']
            adj_greek_df['adj_Nd1'] = st.norm.cdf(adj_greek_df['adj_d1'])
            adj_greek_df['adj_nd1'] = st.norm.pdf(adj_greek_df['adj_d1'])
            adj_greek_df['adj_gamma'] = adj_greek_df['adj_nd1']/greek_df['stock_index_price']/adj_greek_df['adj_sigma_T']
            if option_class == 'VanillaCall':
                adj_greek_df['adj_delta'] = adj_greek_df['adj_Nd1']
            elif option_class == 'VanillaPut':
                adj_greek_df['adj_delta'] = adj_greek_df['adj_Nd1']-1
            else:
                raise ValueError('no option class found')
            self.Zaka_Hedge_df['adj_delta'] += adj_greek_df['adj_delta'] * option_pos
        left_times = self.single_option_info[0]['left_times']
        r = min(r_list)
        self.Zaka_Hedge_df['H0'] = self.lambda_/self.risk_averse/public_df['stock_index_price']/(public_df['sigma'])**2/left_times
        self.Zaka_Hedge_df['H1'] = 1.12*np.power(self.lambda_, 0.31) * np.power(left_times, 0.05) * np.power(np.exp(-r*left_times)/public_df['sigma'], 0.25) * np.power(np.abs(portfolio_greek_df['gamma'])/self.risk_averse, 0.5)
        self.Zaka_Hedge_df['delta_upper_bound'] = self.Zaka_Hedge_df['adj_delta'] + self.Zaka_Hedge_df['H0'] + self.Zaka_Hedge_df['H1']
        self.Zaka_Hedge_df['delta_lower_bound'] = self.Zaka_Hedge_df['adj_delta'] - self.Zaka_Hedge_df['H0'] - self.Zaka_Hedge_df['H1']
        self.Zaka_Hedge_df['adj_cash_delta'] = self.Zaka_Hedge_df['adj_delta']*public_df['stock_index_price']*self.multiplier*self.portfolio_position
        self.Zaka_Hedge_df['cash_delta_up'] = self.Zaka_Hedge_df['delta_upper_bound'] * self.multiplier * public_df['stock_index_price'] * self.portfolio_position
        self.Zaka_Hedge_df['cash_delta_low'] = self.Zaka_Hedge_df['delta_lower_bound'] * self.multiplier * public_df['stock_index_price'] * self.portfolio_position
        return self.Zaka_Hedge_df

    def calculate_target_delta(self):
        Zaka_Hedge_df = self.calculate_target_delta_interval()
        Zaka_Hedge_df.loc[Zaka_Hedge_df.index[0], 'target_delta'] = self.option_greek_df.loc[self.option_greek_df.index[0],'cash_delta']
        for i in range(1, len(Zaka_Hedge_df)):
            Zaka_Hedge_df.loc[Zaka_Hedge_df.index[i], 'target_delta'] = min(max(Zaka_Hedge_df.loc[Zaka_Hedge_df.index[i-1], 'target_delta'], \
                                                                                Zaka_Hedge_df.loc[Zaka_Hedge_df.index[i],'cash_delta_low']), \
                                                                            Zaka_Hedge_df.loc[Zaka_Hedge_df.index[i],'cash_delta_up'])
        self.target_delta = -Zaka_Hedge_df['target_delta']

    def visualize_Zaka(self):
        fig, ax = self.init_canvas([0.08, 0.08, 0.88, 0.87])
        ax.plot(self.Zaka_Hedge_df.index[:-1], self.Zaka_Hedge_df.loc[self.Zaka_Hedge_df.index[:-1], 'adj_cash_delta'], label='cash_delta', color='sandybrown', linewidth=1)
        ax.plot(self.Zaka_Hedge_df.index[:-1], self.Zaka_Hedge_df.loc[self.Zaka_Hedge_df.index[:-1], 'cash_delta_up'], label='cash_delta_up', color='mediumpurple', linewidth=1)
        ax.plot(self.Zaka_Hedge_df.index[:-1], self.Zaka_Hedge_df.loc[self.Zaka_Hedge_df.index[:-1], 'cash_delta_low'], label='cash_delta_low', color='black', linewidth=1)
        ax.plot(self.Zaka_Hedge_df.index[:-1], self.Zaka_Hedge_df.loc[self.Zaka_Hedge_df.index[:-1], 'target_delta'], label='target_delta', color='indianred', linewidth=2)
        ax.legend()
        ax.set_title('Zakamouline策略的delta带与动态调仓', fontsize = 10)
        fig.savefig('../03_img/Zakamouline策略的delta带与动态调仓.jpg')

