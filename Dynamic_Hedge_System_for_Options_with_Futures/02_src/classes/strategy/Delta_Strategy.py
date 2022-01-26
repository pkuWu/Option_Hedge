from .strategyBase import StrategyBase
import numpy as np
import pandas as pd
from scipy import stats as st

#HEDGE ALL
class HedgeAll(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = self.option_greek_df.loc[:, 'cash_delta']

# HEDGE HALF
class HedgeHalf(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = self.option_greek_df.loc[:, 'cash_delta']/2

# Whalley Wilmott method
class WW_Hedge(StrategyBase):
    def __init__(self,lambda_=0.005,risk_averse=1):
        super().__init__()
        self.risk_averse = risk_averse
        self.lambda_ = lambda_
        self.WW_Hedge_df = pd.DataFrame(columns=['H0','delta','delta_upper_bound','delta_lower_bound'])

    def calculate_target_delta_interval(self):
        portfolio_greek_df = self.option_greek_df
        public_df = self.public_df
        left_times_list = []
        r_list = []
        for i in range(len(self.single_option_info)):
            option_obj = self.single_option_info[i]
            left_times_list.append( option_obj['left_times'])
            r_list.append(option_obj['r'])
        left_times = min(left_times_list)
        r = min(r_list)
        self.WW_Hedge_df['H0'] = np.power((3/2*np.exp(r*left_times)*self.lambda_*
                                               public_df['stock_index_price']*np.power(portfolio_greek_df['gamma'],2)/self.risk_averse),1/3)
        self.WW_Hedge_df['delta'] = portfolio_greek_df['delta']
        self.WW_Hedge_df['delta_upper_bound'] = self.WW_Hedge_df['delta']+self.WW_Hedge_df['H0']
        self.WW_Hedge_df['delta_lower_bound'] = self.WW_Hedge_df['delta']-self.WW_Hedge_df['H0']
        return self.WW_Hedge_df

# Zakamouline method
class Zakamouline(StrategyBase):
    def __init__(self,lambda_=0.005,risk_averse=1):
        super().__init__()
        self.lambda_ = lambda_
        self.risk_averse = risk_averse


    def calculate_target_delta_interval(self):
        portfolio_greek_df = self.option_greek_df
        public_df = self.public_df
        self.Zaka_Hedge_df = pd.DataFrame(index = public_df.index,columns=['H0', 'H1', 'adj_delta', 'delta_upper_bound', 'delta_lower_bound','target_delta']).fillna(0)
        left_times_list = []
        r_list = []
        for i in range(len(self.single_option_info)):
            option_obj = self.single_option_info[i]
            option_class = option_obj['option_class']
            greek_df = option_obj['greek_df']
            option_pos = option_obj['option_pos']
            left_times_list.append(option_obj['left_times'])
            r_list.append(option_obj['r'])
            adj_greek_df = pd.DataFrame(columns=['adj_factor_K','adj_sigma','adj_sigma_T','adj_d1','adj_Nd1','adj_nd1','adj_gamma','adj_delta'])
            adj_greek_df['sigma'] = greek_df['sigma']
            adj_greek_df['adj_factor_K'] = -4.76*np.power(self.lambda_,0.78)/np.power(greek_df['left_times'],0.02) * np.power(np.exp(-option_obj['r'] *\
                                            greek_df['left_times']) / adj_greek_df['sigma'],0.25) * np.power(self.risk_averse *\
                                            greek_df['stock_index_price']**2*np.abs(greek_df['gamma']),0.15)
            adj_greek_df['adj_sigma'] = adj_greek_df['sigma']*np.sqrt(1+adj_greek_df['adj_factor_K'])
            adj_greek_df['adj_sigma_T'] = adj_greek_df['adj_sigma']*np.sqrt(greek_df['left_times'])
            adj_greek_df['adj_d1'] = (np.log(greek_df['stock_index_price'] / option_obj['K']) +
                                      option_obj['r']*greek_df['left_times'])/adj_greek_df['adj_sigma_T'] + 0.5 * adj_greek_df['adj_sigma_T']
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
        left_times = min(left_times_list)
        r = min(r_list)
        self.Zaka_Hedge_df['H0'] = self.lambda_/self.risk_averse/public_df['stock_index_price']/(public_df['sigma'])**2/left_times
        self.Zaka_Hedge_df['H1'] = 1.12*np.power(self.lambda_,0.31) * np.power(left_times,0.05) *np.power(np.exp(-r*left_times)/
                                    public_df['sigma'],0.25) * np.power(np.abs(portfolio_greek_df['gamma'])/self.risk_averse,0.5)
        self.Zaka_Hedge_df['delta_upper_bound'] = self.Zaka_Hedge_df['adj_delta'] + self.Zaka_Hedge_df['H0'] + self.Zaka_Hedge_df['H1']
        self.Zaka_Hedge_df['delta_lower_bound'] = self.Zaka_Hedge_df['adj_delta'] - self.Zaka_Hedge_df['H0'] - self.Zaka_Hedge_df['H1']
        self.Zaka_Hedge_df['cash_delta_up'] =self.Zaka_Hedge_df['delta_upper_bound'] * self.multiplier * public_df['stock_index_price']
        self.Zaka_Hedge_df['cash_delta_low'] = self.Zaka_Hedge_df['delta_lower_bound'] * self.multiplier * public_df['stock_index_price']

        return self.Zaka_Hedge_df

    def calculate_target_delta(self):
        Zaka_Hedge_df = self.calculate_target_delta_interval()
        for i in range(len(Zaka_Hedge_df)):
            if self.option_greek_df.loc[i,'delta'] > Zaka_Hedge_df.loc[i,'cash_delta_up'] * self.portfolio_position:
                Zaka_Hedge_df.loc[i,'target_delta'] = Zaka_Hedge_df.loc[i,'cash_delta_up'] * self.portfolio_position - self.option_greek_df.loc[i,'delta']
            elif self.option_greek_df.loc[i,'delta'] < Zaka_Hedge_df.loc[i,'cash_delta_low'] * self.portfolio_position:
                Zaka_Hedge_df.loc[i,'target_delta'] = Zaka_Hedge_df.loc[i,'cash_delta_low'] * self.portfolio_position - self.option_greek_df.loc[i,'delta']
                #target delta为正数，意味着期权组合的delta比对冲带下限更小，需要增加delta；target delta为负数，意味着期权组合的delta超过对冲带上限，需要减少delta
        return Zaka_Hedge_df['target_delta']



