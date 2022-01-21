import numpy as np
from .strategyBase import StrategyBase
class HedgeHalf(StrategyBase):
    def __init__(self):
        super().__init__()

    def get_hedging_position(self,greek_df,stock_price):
        t_length = len(stock_price)
        position = np.zeros((t_length,))
        hedge_all_position = (round(-greek_df.loc[:, 'cash_delta'] / stock_price / self.MULTIPLIER) * self.MULTIPLIER).values
        position[0] = np.round(hedge_all_position[0]/self.MULTIPLIER)*self.MULTIPLIER
        for t_row in range(1,t_length):
            position[t_row] = np.round((hedge_all_position[t_row]+position[t_row-1])/2/self.MULTIPLIER)*self.MULTIPLIER
        return position
