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
simulation_time = 100

if __name__ == '__main__':
    b = Backtest()
    for i in range(simulation_time):
        if i % 100 == 0:
            print(i)
        _, s_dict = b.backtest(s, k, r, T, sigma, gamma, n, strategy='w', v=True)
        if i == 0:
            df_summary = pd.DataFrame(s_dict, index=[0])
        else:
            df_summary = df_summary.append(s_dict, ignore_index=True)

    df_summary['interval'] = pd.cut(df_summary.s, bins=[0, 25, 30, 35, 40, 45, 50, 55, 60, 65, 1000], labels=['25-', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65', '65+'])
    df_summary.groupby('interval')[['fee', 's_pml', 'no_hedge', 's_acoount']].mean().round(2)
    df_summary.groupby('interval').count()/len(df_summary)
