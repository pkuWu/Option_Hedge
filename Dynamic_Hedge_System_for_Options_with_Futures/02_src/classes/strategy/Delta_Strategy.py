from .strategyBase import StrategyBase

class HedgeAll(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = -self.option_greek_df.loc[:, 'cash_delta']

class HedgeHalf(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_target_delta(self):
        self.target_delta = -self.option_greek_df.loc[:, 'cash_delta']/2

