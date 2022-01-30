from .strategyBase import StrategyBase
from abc import abstractmethod
import matplotlib.pyplot as plt


class Delta_StrategyBase(StrategyBase):
    def __init__(self):
        super().__init__()
        self.reset_paras()

    def reset_paras(self):
        self.portfolio_position = None
        self.single_option_info = dict()
        self.option_greek_df = None
        self.public_df = None

    def get_option_info(self, stock_index_code, position, option_basket, greek_df, public_df):
        self.set_paras(stock_index_code)
        self.portfolio_position = position
        self.option_greek_df = greek_df
        self.public_df = public_df
        for i in range(len(option_basket)):
            option_obj = option_basket[i]['option_obj']
            option_pos = option_basket[i]['option_pos']
            option_class = option_basket[i]['option_class']
            greek_df = option_obj.greek_df  # 这里的greek_df是最开始的optionBase/vanilla里有啥就有啥
            option_r = option_obj.r
            option_K = option_obj.K
            left_times = greek_df['left_times']
            self.single_option_info[i] = {'option_class': option_class, 'option_pos': option_pos, 'greek_df': greek_df, 'r': option_r, 'K': option_K, 'left_times': left_times}
        return self

    @abstractmethod
    def calculate_target_delta(self):
        pass

    def get_target_delta(self):
        self.calculate_target_delta()
        return self.target_delta

    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig, ax