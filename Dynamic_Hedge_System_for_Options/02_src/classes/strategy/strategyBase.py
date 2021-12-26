import pandas as pd
from abc import abstractmethod
from ..basicData.basicData import BasicData
class StrategyBase:
    def __init__(self):
        pass

    @abstractmethod
    def get_hedging_position(self,greek_df,stock_price):
        pass