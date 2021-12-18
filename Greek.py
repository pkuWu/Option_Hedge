""" 
@Time    : 2021/12/7 21:32
@Author  : Carl
@File    : Greek.py
@Software: PyCharm
"""
import numpy as np
import scipy.stats as si

class Greek:
    def __init__(self):
        """
        :param n: 看涨期权取1 看跌期权取-1
        """
        self.s = 42
        self.k = 40
        self.r = 0.1
        self.T = 0.5
        self.sigma = 0.2
        self.n = 1

    def d(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2):
        d1 = (np.log(s/k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return (d1,d2)

    def delta(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2, n=1):
        d1 = self.d(s, k, r, T, sigma)[0]
        delta = n * si.norm.cdf(n * d1)
        return delta

    def gamma(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2):
        d1 = self.d( s, k, r, T, sigma)[0]
        gamma = si.norm.pdf(d1) / (s * sigma * np.sqrt(T))
        return gamma

    def vega(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2):
        d1 = self.d(s, k, r, T, sigma)[0]
        ##
        vega = (s * si.norm.pdf(d1) * np.sqrt(T)) / 100
        return vega

    def theta(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2, n=1):
        (d1, d2) = self.d(s, k, r, T, sigma)
        theta = (-1 * (s * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - n * r * k * np.exp(-r * T) * si.norm.cdf(n * d2)) / 252
        return theta

    def BS(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2, n=1):
        (d1, d2) = self.d(s, k, r, T, sigma)
        if n == 1:
            return s * si.norm.cdf(d1) - k * np.exp(-r * T) * si.norm.cdf(d2)
        if n == -1:
            return k * np.exp(-r * T) * si.norm.cdf(-d2) - s * si.norm.cdf(-d1)