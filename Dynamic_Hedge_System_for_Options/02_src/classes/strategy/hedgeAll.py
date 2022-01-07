from .strategyBase import StrategyBase
class HedgeAll(StrategyBase):
    def __init__(self):
        super().__init__()

    def get_hedging_position(self,greek_df,stock_price):
        return round(-greek_df.loc[:,'cash_delta']/stock_price/self.MULTIPLIER)*self.MULTIPLIER