from .strategyBase import StrategyBase


class Dominant(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        self.future_weight_dict['weight_info'].iloc[:, 0] = 1

class Current_Month(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        self.future_weight_dict['weight_info'].iloc[:, 1] = 1

class Next_Month(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        self.future_weight_dict['weight_info'].iloc[:, 2] = 1

class Current_Season(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        self.future_weight_dict['weight_info'].iloc[:, 3] = 1

class Next_Season(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        self.future_weight_dict['weight_info'].iloc[:, 4] = 1

class Holding_Weighted(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        weight_df = self.future_data['holding'].loc[self.trade_dates]
        weight_df.iloc[:, 0] = 0
        self.future_weight_dict['weight_info'] = weight_df.div(weight_df.sum(axis=1), axis='rows')

class Volume_Weighted(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        weight_df = self.future_data['volume'].loc[self.trade_dates]
        weight_df.iloc[:, 0] = 0
        self.future_weight_dict['weight_info'] = weight_df.div(weight_df.sum(axis=1), axis='rows')