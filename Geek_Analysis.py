""" 
@Time    : 2021/12/7 22:02
@Author  : Carl
@File    : Geek_Analysis.py
@Software: PyCharm
"""
from Greek import Greek
import matplotlib.pyplot as plt
import numpy as np
#
def Greek_Plot(Theta_List_real, Theta_List_weak, Theta_List_par, scale, Greek='Theta', parameter='T'):
    plt.figure(dpi=120, figsize=(15, 10))
    plt.plot(scale, Theta_List_real, label='In the Money')
    plt.plot(scale, Theta_List_weak, label='Out of the Money')
    plt.plot(scale, Theta_List_par, label='At the Money')
    plt.legend(loc='best')
    plt.xlabel(parameter)
    plt.ylabel(Greek)
    # plt.title('Value Status')
    plt.show()
#
# Default Parameter
s = 42
k = 40
r = 0.1
T = 0.5
sigma = 0.2
n = 1
#
MF = Greek()
#
# Theta
# 价值状态(实， 平， 虚)

# T
Time_Scale = np.linspace(0.01, 5, 101)
Theta_List_real = []
Theta_List_weak = []
Theta_List_par = []
for T in Time_Scale:
    Theta_real = MF.theta(T=T, s=45)
    Theta_weak = MF.theta(T=T, s=35)
    Theta_par = MF.theta(T=T, s=40)
    Theta_List_real.append(Theta_real)
    Theta_List_weak.append(Theta_weak)
    Theta_List_par.append(Theta_par)

Greek_Plot(Theta_List_real, Theta_List_weak, Theta_List_par, scale=Time_Scale, parameter='T')
#
# # Sigma
Sigma_Scale = np.linspace(0.001, 2, 1000)
Theta_List_real = []
Theta_List_weak = []
Theta_List_par = []
for Sigma in Sigma_Scale:
    Theta_real = MF.theta(sigma=Sigma, s=45)
    Theta_weak = MF.theta(sigma=Sigma, s=35)
    Theta_par = MF.theta(sigma=Sigma, s=40)
    Theta_List_real.append(Theta_real)
    Theta_List_weak.append(Theta_weak)
    Theta_List_par.append(Theta_par)

Greek_Plot(Theta_List_real, Theta_List_weak, Theta_List_par, scale=Sigma_Scale, parameter='Sigma')
#
# Stock Price
Price_Scale = np.linspace(10, 100, 1000)
Theta_List = []
for price in Price_Scale:
    Theta = MF.theta(s=price)
    Theta_List.append(Theta)

plt.figure(figsize=(15, 10))
plt.plot(Price_Scale, Theta_List, label='Theta')
plt.legend(loc='best')
plt.xlabel('Price')
plt.ylabel('Theta')
# plt.title('Value Status')
plt.show()
#
# # Vega

#
# # T
Time_Scale = np.linspace(0.01, 5, 101)
Vega_List_real = []
Vega_List_weak = []
Vega_List_par = []
for T in Time_Scale:
    Vega_real = MF.vega(T=T, s=45)
    Vega_weak = MF.vega(T=T, s=35)
    Vega_par = MF.vega(T=T, s=40)
    Vega_List_real.append(Vega_real)
    Vega_List_weak.append(Vega_weak)
    Vega_List_par.append(Vega_par)
#
Greek_Plot(Vega_List_real, Vega_List_weak, Vega_List_par, scale=Time_Scale, Greek='Vega', parameter='T')
#
#
# # Sigma
Sigma_Scale = np.linspace(0.001, 2, 1000)
Vega_List_real = []
Vega_List_weak = []
Vega_List_par = []
for Sigma in Sigma_Scale:
    Vega_real = MF.vega(sigma=Sigma, s=45)
    Vega_weak = MF.vega(sigma=Sigma, s=35)
    Vega_par = MF.vega(sigma=Sigma, s=40)
    Vega_List_real.append(Vega_real)
    Vega_List_weak.append(Vega_weak)
    Vega_List_par.append(Vega_par)

Greek_Plot(Vega_List_real, Vega_List_weak, Vega_List_par, scale=Sigma_Scale, Greek='Vega', parameter='Sigma')
#
# # Stock Price
Price_Scale = np.linspace(10, 100, 1000)
Vega_List = []
for price in Price_Scale:
    Vega = MF.vega(s=price)
    Vega_List.append(Vega)

plt.figure(figsize=(15, 10))
plt.plot(Price_Scale, Vega_List, label='Vega')
plt.legend(loc='best')
plt.xlabel('Price')
plt.ylabel('Vega')
# plt.title('Value Status')
plt.show()

# Zakamouline Hedge Strategy
from Strategy.WW import Whalley_Wilmott
from Strategy.Zakamouline import Zakamouline
import matplotlib.pyplot as plt

def plot_hedge(k,r,T,Lambda,gamma,n, strategy='w'):
    s = np.linspace(k-20, k+30, 500)
    plt.figure(figsize=(15, 10))
    if strategy == 'w':
        method = Whalley_Wilmott()
        upper, delta, lower = method.WW(r=r,T=T,Lambda=Lambda,s=s,gamma=gamma,n=n)
        plt.plot(delta, upper, color='r')
        plt.plot(delta, lower, color='r')
        plt.plot(delta, delta, color='black')
    elif strategy == 'z':
        method = Zakamouline()
        upper, adj_delta, lower = method.ZM_Boundary(s=s, T=T, gamma=gamma, Lambda=Lambda, k=k, r=r, sigma=sigma, n=n)
        delta = method.delta(s=s, n=n)
        plt.plot(delta, upper, color='r')
        plt.plot(delta, lower, color='r')
        plt.plot(delta, adj_delta, color='r', linestyle='dashed')
        plt.plot(delta, delta, color='black')

    plt.xlabel('Delta')
    plt.ylabel('Hedge Belt')
    if n == 1:
        plt.title(f'Call Option: Lambda={Lambda} gamma={gamma}')
    elif n == -1:
        plt.title(f'Put Option: Lambda={Lambda} gamma={gamma}')
    plt.savefig('./Figure/HedgeBelt.png')
    plt.show()

# ZZ Hedge Strategy
plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=0.2,n=-1, strategy='z')

