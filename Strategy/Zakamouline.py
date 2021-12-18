""" 
@Time    : 2021/12/9 9:44
@Author  : Carl
@File    : Zakamouline.py
@Software: PyCharm
"""
import pandas as pd

from Greek import Greek
import numpy as np

class Zakamouline(Greek):
    def __init__(self):
        super(Zakamouline, self).__init__()

    def K(self, s, r, T, sigma, Lambda, gamma, Gamma):
        return -4.76 * Lambda**0.78 / T**0.02 * (np.exp(-r * T) / sigma)**0.25 * (gamma * s**2 * np.absolute(Gamma))**0.15

    def Adj_Sigma(self, s, r, T, sigma, Lambda, gamma, Gamma):
        return sigma * np.sqrt(self.K(s, r, T, sigma, Lambda, gamma, Gamma) + 1)

    def H0(self, s, T, sigma, Lambda, gamma):
        return Lambda / (gamma * s * sigma ** 2 * T)

    def H1(self, r, T, sigma, Lambda, gamma, Gamma):
        return 1.12 * Lambda**0.31 * T**0.05 * (np.exp(-r * T) / sigma)**0.25 * (np.absolute(Gamma) / gamma)**0.5

    def ZM_Boundary(self, s=42, k=40, r=0.1, T=0.5, sigma=0.2, Lambda=0.02, gamma=1, n=1):
        Gamma = super().gamma(s=s, k=k, r=r, T=T, sigma=sigma)
        H1 = self.H1(r, T, sigma, Lambda, gamma, Gamma)
        H0 = self.H0(s, T, sigma, Lambda, gamma)
        adj_sigma = self.Adj_Sigma(s, r, T, sigma, Lambda, gamma, Gamma)
        adj_delta = super().delta(s, k, r, T, adj_sigma, n)
        return (adj_delta-H0-H1, adj_delta, adj_delta+H0+H1)

    # def hedgebelt_plot(self, s=42, k=42, r=0.1, T=0.5, sigma=0.2, Lambda=0.02, gamma=1):
    #     Gamma = self.gamma(s=s, k=k, r=r, T=T, sigma=sigma)
    #     H1 = self.H1(r, T, sigma, Lambda, gamma, Gamma)
    #     H0 = self.H0(s, T, sigma, Lambda, gamma)

