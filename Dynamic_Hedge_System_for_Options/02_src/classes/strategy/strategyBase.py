import pandas as pd
from abc import abstractmethod
from ..basicData.basicData import BasicData
import matplotlib.pyplot as plt

class StrategyBase:
    def __init__(self):
        self.MULTIPLIER = 100

    def hedge_visualization(self, greek_df):
        df_plot = self.df_hedge.loc[:, ['delta', 'position_rate', 'low_bound', 'up_bound']]
        df_plot.index = greek_df['left_times']
        df_plot.loc[:, ['delta_value', 'gamma_value', 'theta_value','vega_value']] = greek_df.loc[:, ['delta_value', 'gamma_value', 'theta_value','vega_value']].values
        fig, ax1 = plt.subplots(figsize=(15, 10))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Delta')
        ax1.set_ylim(0, 1.5)
        df_plot.loc[:, ['position_rate', 'low_bound', 'up_bound']].plot(ax=ax1)
        ax1.legend(loc='upper left')
        ax2 = ax1.twinx()
        ax2.set_ylabel('Pnl')
        ax2.legend(loc='upper right')
        df_plot.loc[:, ['delta_value', 'gamma_value', 'theta_value','vega_value']].plot(ax=ax2)
        plt.show()

    @abstractmethod
    def get_hedging_position(self,greek_df,stock_price):
        pass