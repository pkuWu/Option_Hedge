# 期权对冲回测系统

该系统预备实现的功能有：

1. 针对香草期权、单边看涨/看跌鲨鱼鳍期权、autocall、安全气囊期权的对冲回测
2. 输入股票指数、产品类型以及对应的产品参数，设定对冲策略后，运行回测，输出可视化分析报告

------

## 一、期权产品介绍

这里主要写：期权收益结构、期权希腊值计算方法

------

## 二、回测算法介绍

这里主要写：对于已经给出的stock_position目标序列，如何计算各项收益、交易成本、账户核算的细节

------

## 三、对冲策略介绍

每新增一个对冲策略，都要在这里把策略名以及对应的stock_position计算方法详细地写在这里

------

## 四、对冲回测分析框架

1、股指与股指期货头寸分析-折线图

​	股指期货头寸 total_future_position：每日各股指期货头寸之和

​	股指头寸 total_index_position：股指期货月合约在等value的的条件下对应的股指头寸数目
$$
total\_index\_position_{t}=\Sigma_i index\_position_{i,t} \\= \Sigma_i (future\_price_{i,t}\times future\_position_{i,t}/index\_price_{i,t})
$$
2、交易成本分析（除以名义本金）-堆叠图

​	名义本金
$$
notional=option\_portfolio\_position\times multiplier\times stock\_index\_price_{0}
$$
​	总交易成本：所有股指期货合约在每个时点上调仓时产生的总交易成本
$$
total\_trading\_cost_{t}
=\Sigma_i single\_trading\_cost_{i,t} 
\\= \Sigma_i (|future\_position_{i,t}-future\_position_{i,t-1}|\times future\_price_{i,t}\times multiplier\times tr)
$$
​	动态对冲交易成本：基于股指仓位，得到因指数点位变动而导致delta动态对冲中股指期货头寸比例发生变化，	而带来的交易成本
$$
hedging\_trading\_cost_{t}\\=|total\_index\_position_{t}-total\_index\_position_{t-1}|\times index\_price_{t} \times multiplier \times tr
$$
​	展期交易成本：总成本扣除动态对冲交易成本后剩余的部分
$$
rollover\_trading\_cost_{t}=total\_trading\_cost_{t}-hedging\_trading\_cost_{t}
$$
