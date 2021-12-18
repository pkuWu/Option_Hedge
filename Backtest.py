""" 
@Time    : 2021/12/11 9:05
@Author  : Carl
@File    : Backtest.py
@Software: PyCharm
"""
import numpy as np
import pandas as pd
from numpy import random
from Strategy.Zakamouline import Zakamouline
import matplotlib.pyplot as plt
from Strategy.WW import Whalley_Wilmott

class Backtest(Zakamouline, Whalley_Wilmott):
    def __init__(self):
        super(Backtest, self).__init__()

    def simulation(self, s, sigma=0.5, T=1, freq='min'):
        if freq == 'min':
            n = int(T * 252 * 4 * 60)
        elif freq == 'hour':
            n = int(T * 252 * 4)
        elif freq == 'second':
            n = int(T * 252 * 4 * 3600)
        elif freq == 'day':
            n = int(T * 252)
        d_s = random.randn(n) * np.sqrt(sigma * T / n) - 0.5 * (T / n) * sigma**2
        return s * np.exp(d_s.cumsum())

    def position(self, delta, upper, lower, size=100000):
        pos = (delta[0] * size) // 100 * 100
        r_pos = pos / size
        df_pos = pd.DataFrame(data=[(0, delta[0], pos, r_pos)],
                              columns=['i', 'delta', 'position', 'position_ratio'])
        for i in range(1, len(delta)):
            if r_pos > upper[i] or r_pos < lower[i]:
                pos = (delta[i] * size) // 100 * 100
                r_pos = pos / size
                df_pos = df_pos.append([{'i': i, 'delta': delta[i], 'position': pos, 'position_ratio': r_pos}],
                                       ignore_index=True)
        return df_pos

    def transaction(self, delta, upper, lower, df_delta, size=100000):
        df_transaction = self.position(delta, upper, lower, size=size)
        df_transaction['d_position'] = df_transaction.position - df_transaction.position.shift(1, fill_value=0)
        df_transaction['s'] = df_delta.loc[df_transaction.i, 's'].values
        df_transaction['fee'] = np.abs(df_transaction.d_position) * df_transaction.s * 0.02
        df_transaction['s_pml'] = - df_transaction.d_position * df_transaction.s
        df_transaction['account'] = df_transaction.s_pml.cumsum()
        df_transaction.index = df_transaction.i
        return df_transaction

    def montecarlo_vis(self, sim_s):
        plt.figure(figsize=(15, 10))
        plt.plot(sim_s, label='stock price')
        plt.xlabel('Time (Month)')
        plt.ylabel('Stock Price')
        plt.title('Monte Carlo Simulation')
        plt.legend()
        plt.savefig('./Montecarlo.png')
        # plt.show()

    def transaction_vis(self, df_plot, strategy='z'):
        # fig = plt.figure(figsize=(15, 10))
        df_plot.set_index(df_plot['T']*12, inplace=True)
        ax = df_plot[['delta', 'lower', 'upper', 'position']].plot(figsize=(15, 10))
        ax.set_ylim(-2, 2)
        ax.invert_xaxis()
        ax.set_xlabel('Time')
        ax.set_ylabel('Delta')
        if strategy=='z':
            plt.title('Zakamouline Hedge')
            plt.savefig('./Figure/Zekamouline.png')
        else:
            plt.title('WW Hedge')
            plt.savefig('./Figure/WW.png')
        # plt.show()

    # def hedgebelt_plot(self, delta, upper, lower):
    #     supper = pd.Series(upper, index=delta)
    #     slower = pd.Series(lower, index=delta)
    #     plt.figure(figsize=(15, 10))
    #     plt.plot(supper.sort_index())
    #     plt.plot(slower.sort_index())
    #     plt.plot(np.linspace(-1, 2, 1000), np.linspace(-1, 2, 1000), c='r')
    #     plt.ylim([-1, 1])
    #     plt.xlim([-1, 1])
    #     plt.xlabel('Delta')
    #     plt.ylabel('Hedge Belt')
    #     plt.title('Hedge Belt')
    #     plt.savefig('./Hedgebelt.png')
    #     # plt.show()


    def backtest(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2, gamma=1, n=1, freq='min', Lambda=0.02, size=100000, v=False, strategy='z'):
        c0 = self.BS(s, k, r, T, sigma, n)
        sim_s = self.simulation(s, sigma, T, freq)
        sim_s = pd.Series(sim_s, index=np.linspace(0, T * 12, len(sim_s)))
        sim_T = sim_s.index[:0:-1] / 12
        delta = self.delta(s=sim_s.values[:-1], T=sim_T)
        if strategy == 'z':
            (lower, adj_delta, upper) = self.ZM_Boundary(s=sim_s.values[:-1], T=sim_T, gamma=gamma, Lambda=Lambda, k=k, r=r, sigma=sigma, n=n)
        elif strategy == 'w':
            (lower, adj_delta, upper) = self.WW(s=sim_s.values[:-1], r=r, T=sim_T, gamma=gamma, Lambda=Lambda, n=n)
        df_delta = pd.DataFrame(delta, columns=['delta'])
        df_delta['lower'], df_delta['upper'], df_delta['s'], df_delta['T'] = lower, upper, sim_s.values[:-1], sim_T
        df_transaction = self.transaction(delta, upper, lower, df_delta, size)
        df_delta['position'] = df_transaction.position_ratio
        df_delta.fillna(method='pad', inplace=True)
        if v:
            self.montecarlo_vis(sim_s)
            self.transaction_vis(df_delta.copy(), strategy=strategy)
        sn = df_delta.s.values[-1]
        if n == 1:
            p_option = c0 + k - sn if k < sn else c0
        elif n == -1:
            p_option = c0 + sn - k if k > sn else c0
        sum_dict = df_transaction[['fee', 's_pml']].sum().to_dict()
        sum_dict.update({'s': df_delta.s.values[-1], 'no_hedge': p_option*size, 's_acoount': sn * df_transaction.position.values[-1]})
        return df_transaction, sum_dict