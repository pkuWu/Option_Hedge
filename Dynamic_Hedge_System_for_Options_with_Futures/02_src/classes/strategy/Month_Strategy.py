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
        weight_df['sum_by_row'] = weight_df.apply(lambda x: x.sum(), axis=1)
        for i in range(len(weight_df.columns)):
            weight_df.iloc[:, i] = weight_df.iloc[:, i] / weight_df.loc[:, 'sum_by_row']
        self.future_weight_dict['weight_info'] = weight_df.iloc[:, :(len(weight_df.columns)-1)]

class Volume_Weighted(StrategyBase):
    def __init__(self):
        super().__init__()

    def calculate_future_weight(self):
        weight_df = self.future_data['volume'].loc[self.trade_dates]
        weight_df.iloc[:, 0] = 0
        weight_df['sum_by_row'] = weight_df.apply(lambda x: x.sum(), axis=1)
        for i in range(len(weight_df.columns)):
            weight_df.iloc[:, i] = weight_df.iloc[:, i] / weight_df.loc[:, 'sum_by_row']
        self.future_weight_dict['weight_info'] = weight_df.iloc[:, :(len(weight_df.columns)-1)]