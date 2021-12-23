import numpy as np
import pandas as pd
import os
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from ..basicData.basicData import BasicData
from ..options.OptionData import OptionData
from ..strategy import *
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class BacktestFramework:
    TR = 0.0002
    def __init__(self):
        self.reset()
        self.CLASS_PATH = __file__
        self.REPORT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'report')
        self.EXCEL_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'excel')

    def reset(self):
        self.option_data = OptionData()
        self.set_strategy()

    def set_strategy(self, strategy_name=''):
        self.strategy_name = strategy_name
        self.strategy = None if not strategy_name else eval(strategy_name)()

    def set_option(self,option_class,option_position,**option_paras):
        self.option_data.set_option_by_dict(option_class,option_position,option_paras)

    def run_backtest(self):
        pass
        
    def export_exceldata(self):
        current_time = str(datetime.now()).replace(':', '：')
        self.check_folder(self.EXCEL_FOLDER)
        report_name = os.path.join(self.EXCEL_FOLDER,''))
        self.backtest_df.to_excel(report_name,index=True)

    def visualize(self,report=False):
        if report:
            current_time = str(datetime.now()).replace(':', '：')
            self.check_folder(self.REPORT_FOLDER)
            report_name = os.path.join(self.REPORT_FOLDER,'')
            with PdfPages(report_name) as pdf:
                pass

    @staticmethod
    def init_canvas(rect=[0.05, 0.05, 0.9, 0.9]):
        fig = plt.figure(figsize=(10, 5.7), dpi=300)
        ax = fig.add_axes(rect=rect)
        return fig,ax
        
    @staticmethod
    def cal_MDD(series):
        return np.max(series.cummax()-series)
    
    @staticmethod
    def check_folder(temp_folder):
        if not os.path.isdir(temp_folder):
            BacktestFramework.make_folder(temp_folder)
            
    @staticmethod
    def make_folder(temp_folder):
        if not os.path.isdir(os.path.dirname(temp_folder)):
            BacktestFramework.make_folder(os.path.dirname(temp_folder))
        os.makedirs(temp_folder)