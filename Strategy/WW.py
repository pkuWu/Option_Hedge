import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from Greek import Greek


class Whalley_Wilmott(Greek):
    def __init__(self):
        super(Whalley_Wilmott, self).__init__()

    def h0(self,r,T,Lambda,s,gamma):
        Gamma = super().gamma(s=s, k=40, r=r, T=T, sigma=0.2)
        return (3/2*np.exp(-r*T)*Lambda*s*Gamma**2/gamma)**(1/3)

    def WW(self,r,T,Lambda,s,gamma,n):

        # Gamma=super().gamma(s=42, k=40, r=0.1, T=0.5, sigma=0.2)
        H0=self.h0(r,T,Lambda,s,gamma)
        Delta=super().delta(s=s, k=40, r=r, T=T, sigma=0.2, n=n)
        return(Delta-H0,Delta,Delta+H0)

def plot_hedge(k,r,T,Lambda,gamma,title,j,n):
    """
    :param k: Strike price of option
    :param r: Risk free rate
    :param T: T is the time limit of the option
    :param Lambda: Lambda is the transaction cost
    :param gamma: gamma is the risk averse coefficient
    :param title: title is the title of the figure
    :param j: j is the num of the figure
    :param n: n = 1, call option; n = -1, put option
    :return: figure j
    """
    s = np.arange(k-20,k+20,1)
    upper = np.zeros(len(s))
    delta = np.zeros(len(s))
    lower = np.zeros(len(s))
    for i in range(len(s)):
       upper[i],delta[i],lower[i]=ww.WW(r=r,T=T,Lambda=Lambda,s=s[i],gamma=gamma,n=n)
    mpl.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(delta,upper,color='r')
    plt.plot(delta,lower,color='r')
    plt.plot(delta,delta,color='black')
    plt.xlabel('Delta')
    plt.ylabel('对冲带')
    plt.title(title)
    plt.savefig('./Figure/对冲带'+str(j)+'.png')
    plt.show()

# ww = Whalley_Wilmott()
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=0.2,title='',j=1,n=1)
#
# #比较不同交易成本下的对冲带
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=0.2,title='lambda=0.02',j=2,n=1)
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.005,gamma=0.2,title='lambda=0.005',j=3,n=1)
#
# #比较不同风险厌恶系数下的对冲带
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=0.2,title='gamma=0.02',j=4,n=1)
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=2,title='gamma=2',j=5,n=1)
#
# #比较看涨期权和看跌期权的对冲带
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=0.2,title='call option',j=6,n=1)
# plot_hedge(k=40,r=0.1,T=1,Lambda=0.02,gamma=0.2,title='put option',j=7,n=-1)

