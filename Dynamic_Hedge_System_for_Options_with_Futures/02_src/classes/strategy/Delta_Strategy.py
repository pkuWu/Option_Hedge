from .strategyBase import StrategyBase
import numpy as np
import pandas as pd


#HEDGE ALL
class HedgeAll(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = self.option_greek_df.loc[:, 'cash_delta']
        return self.target_delta

# HEDGE HALF
class HedgeHalf(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = self.option_greek_df.loc[:, 'cash_delta']/2
        return self.target_delta

# Whalley Wilmott method
class WW_Hedge(StrategyBase):
    def __init__(self,lambda_=0.005,risk_averse=1):
        super().__init__()
        self.risk_averse = risk_averse
        self.lambda_ = lambda_
        self.WW_Hedge_df = pd.DataFrame(columns=['H0','delta','delta_upper_bound','delta_lower_bound'])

    def calculate_target_delta_interval(self):
        greek_df = self.option_greek_df
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
                                               public_df['stock_index_price']*np.power(greek_df['gamma'],2)/self.risk_averse),1/3)
        self.WW_Hedge_df['delta'] = greek_df['delta']
        self.WW_Hedge_df['delta_upper_bound'] = self.WW_Hedge_df['delta']+self.WW_Hedge_df['H0']
        self.WW_Hedge_df['delta_lower_bound'] = self.WW_Hedge_df['delta']-self.WW_Hedge_df['H0']
        return self.WW_Hedge_df

