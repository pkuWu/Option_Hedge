from .strategyBase import StrategyBase

class HedgeAll(StrategyBase):
    def __init__(self,option):
        super().__init__()
        self.get_option_info(option)

    def calculate_target_delta(self):
        self.target_delta = -self.option_greek_df['cash_delta']
        return self.target_delta



class HedgeHalf(StrategyBase):
    def __init__(self,option):
        super().__init__()
        self.get_option_info(option)

    def calculate_target_delta(self):
        self.target_delta = -self.option_greek_df['cash_delta']/2
        return self.target_delta

