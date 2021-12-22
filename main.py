""" 
@Time    : 2021/12/7 21:32
@Author  : Carl
@File    : main.py
@Software: PyCharm
"""
import pandas as pd
from Backtest import Backtest

# Parameters
s = 42
k = 40
r = 0.1
T = 0.5
sigma = 0.2
gamma = 1.5
n = 1
simulation_time = 500

if __name__ == '__main__':
    b = Backtest()
    for i in range(simulation_time):
        if i % 100 == 0:
            print(i)
        _, s_dict = b.backtest(s, k, r, T, sigma, gamma, n, strategy='w', v=False)
        if i == 0:
            df_summary = pd.DataFrame(s_dict, index=[0])
        else:
            df_summary = df_summary.append(s_dict, ignore_index=True)

        b.result_output(df_summary, k=k)
