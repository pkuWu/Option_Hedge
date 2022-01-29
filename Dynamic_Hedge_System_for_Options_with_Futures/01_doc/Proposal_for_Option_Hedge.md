# 期权对冲回测系统

该系统预备实现的功能有：

1. 针对香草期权、单边看涨/看跌鲨鱼鳍期权、autocall、安全气囊期权的对冲回测
2. 输入股票指数、产品类型以及对应的产品参数，设定对冲策略后，运行回测，输出可视化分析报告

------

## 一、期权产品介绍

**期权组合Option_Contract包括构建以下种类的期权：**

```
option_type = {'VanillaCall': '看涨期权',
               'VanillaPut': '看跌期权',
               'BullCallSpread': '牛市看涨差价',
               'BullPutSpread': '牛市看跌差价',
               'BearCallSpread': '熊市看涨差价',
               'BearPutSpread': '熊市看跌差价',
               'BoxSpread': '盒式差价',
               'Straddle': '跨式组合',
               'Strangle': '宽跨式组合',
               'ButterflyCallSpread': '蝶式看涨差价',
               'ButterflyPutSpread': '蝶式看跌差价',
               'CalendarCallSpread': '看涨期权构造的日历差价',
               'CalendarPutSpread': '看跌期权构造的日历差价',
               'RatioCallSpread': '看涨比率差价',# 看涨比率差价空头、看跌比率差价空头
               'RatioPutSpread': '看跌比率差价'}
```

（注：默认position输入为正时是看涨比率差价空头、看跌比率差价空头、其他组合多头。）

假设无风险利率r=4%。

**香草期权greeks计算方法：**

*看涨期权：*

(1) delta
$$
delta = N(d_1)\\ d_1=\frac{ln(\frac{S}{K})+(r+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}},d_2=d_1-\sigma\sqrt{T}
$$
(2) gamma
$$
gamma=\frac{N'(d_1)}{S\sigma\sqrt{T}}
$$
(3) theta
$$
theta=-\frac{SN'(d_1)\sigma}{2\sqrt{T}}-rKe^{-rT}N(d_2)
$$
(4) vega
$$
vega=S\sqrt{T}N'(d_1)
$$
*看跌期权：*

(1) delta
$$
delta = N(d_1)-1
$$
(2) gamma
$$
gamma=\frac{N'(d_1)}{S\sigma\sqrt{T}}
$$
(3) theta
$$
theta=-\frac{SN'(d_1)\sigma}{2\sqrt{T}}+rKe^{-rT}N(-d_2)
$$
(4) vege
$$
vega=S\sqrt{T}N'(d_1)
$$
**香草期权cash_greeks计算方法：**

(1) cash_delta
$$
cash\_delta=delta\times S\times multiplier
$$
(2) cash_gamma
$$
cash\_gamma=gamma\times \frac{S^2}{100} \times multiplier
$$
(3) cash_theta
$$
cash\_theta=\frac{theta\times multiplier}{252}
$$
**期权组合greeks计算**：组合内香草期权的greeks线性相加。

**期权收益分解：**

(1) option_pnl
$$
option\_pnl=\Delta(option\_value)=\Delta(option\_price\times multiplier)\\=\Delta(SN{(d_1)}-Ke^{-rT}N(d_2)\times multiplier)
$$
(2) delta_pnl
$$
delta\_pnl=delta\times \Delta S
$$
(3) gamma_pnl
$$
gamma\_pnl=\frac{1}{2}\times gamma\times (\Delta S)^2
$$
(4) theta_pnl
$$
theta\_pnl=theta\times \Delta t
$$
(5) vega_pnl
$$
vega\_pnl=vega\times \Delta \sigma
$$
(6) high_order_pnl
$$
high\_order\_pnl=option\_pnl-delta\_pnl-gamma\_pnl-theta\_pnl-vega\_pnl
$$


------

## 二、回测算法介绍

基于对冲策略得到的各个期权合约target_future_position进行策略收益回测，**功能主要包括**：

1. 期货持仓计算
2. 交易成本拆解
3. 期货对冲端收益拆解
4. 各部分收益累和计算
5. 保证金账户和现金账户核算
6. 资金借贷利息损益计算

以下列出**比率数据假设**：

(1) 交易成本率 

​	tr=0.0023%

(2) 保证金率 

​	mr=14%

(3) 货币借贷利率（资金成本率）

​	ir=2% （年化）

(4) 保证金账户上限比率 

​	max_ratio=1.5

以下列出**有关计算交易成本、各项收益及账户核算的各项数据的计算方式及解释**：

**(1) future_position**

​	期货的目标头寸。

**(2) future_price**

​	期货的（收盘）点位。

**(3) future_value**

​	期货价值：调仓后持有的期货头寸价值。
$$
future\_value_{t}=\Sigma_i future\_price_{i,t} \times future\_position_{i,t} \times multiplier
$$
**(4) index_price**

​	股指的（收盘）点位。

**(5) total_index_position**

​	股指头寸：股指期货月合约在等value的的条件下对应的股指头寸数目。
$$
total\_index\_position_{t}=\Sigma_i index\_position_{i,t} \\= \Sigma_i (future\_price_{i,t}\times future\_position_{i,t}/index\_price_{i,t})
$$
**(6) notional**

​	名义本金：
$$
notional=option\_portfolio\_position\times multiplier\times stock\_index\_price_{0}
$$
**(7) single_trading_cost**

​	每个单独的股指期货合约在每个时点上调仓时产生的交易成本。
$$
single\_trading\_cost_{i,t} 
\\= |future\_position_{i,t}-future\_position_{i,t-1}|\times future\_price_{i,t}\times multiplier\times tr
$$
**(8) total_trading_cost**

​	总交易成本：所有股指期货合约在每个时点上调仓时产生的总交易成本。
$$
total\_trading\_cost_{t}
=\Sigma_i single\_trading\_cost_{i,t} 
\\= \Sigma_i (|future\_position_{i,t}-future\_position_{i,t-1}|\times future\_price_{i,t}\times multiplier\times tr)
$$
**(9) hedging_trading_cost**

​	动态对冲交易成本：基于股指仓位，得到因指数点位变动而导致delta动态对冲中股指期货头寸比例发生变化而带来的交易成本
$$
hedging\_trading\_cost_{t}\\=|total\_index\_position_{t}-total\_index\_position_{t-1}|\times index\_price_{t} \times multiplier \times tr
$$
**(10) rollover_trading_cost**

​	展期交易成本：总成本扣除动态对冲交易成本后剩余的部分。
$$
rollover\_trading\_cost_{t}=total\_trading\_cost_{t}-hedging\_trading\_cost_{t}
$$
**(11) single_future_pnl**

​	第i个股指期货在第t个时间段上产生的pnl。
$$
single\_future\_pnl_{i,t}=(future\_price_{i,t}-future\_price_{i,t-1})×future\_position_{i,t-1}×multiplier
$$
**(12) total_future_pnl**

​	股指期货组合在第t个时间段上产生的整体pnl。
$$
total\_future\_pnl_{t}=\Sigma_{i}single\_future\_pnl_{i,t}
$$
**(13) index_pnl**

​	股指对冲收益：
$$
index\_pnl_{t}=(index\_price_{t}-index\_price_{t-1})×total\_index\_position_{t-1}×multiplier
$$
**(14) basis_pnl**

​	基差收益：
$$
basic\_pnl_{t}=total\_future\_pnl_{t}-index\_pnl_{t}
$$
**(15) cum_total_pnl**

​	期货对冲端累积收益：
$$
cum\_total\_pnl_{t}=\Sigma_{j=0}^ttotal\_future\_pnl_{j}
$$
**(16) cum_index_pnl**

​	对冲端指数累积收益：
$$
cum\_index\_pnl_{t}=\Sigma_{j=0}^tindex\_pnl_{j}
$$
**(17) cum_basis_pnl**

​	基差累积收益：
$$
cum\_basis\_pnl_{t}=\Sigma_{j=0}^tbasis\_pnl_{j}
$$
**(18) margin_account**

​	保证金账户数额：建仓时，使保证金账户的存款恰好等于维持保证金要求的数额，在随后的时点上，如果期货点位变动，导致保证金账户水平低于维持保证金要求的水平，则补充保证金至维持保证金水平；如果期货点位变动，导致保证金账户水平高于维持保证金要求的水平的max_ratio倍，则将保证金账户水平降低至维持保证金要求的水平的max_ratio倍；如果期货点位变动，导致保证金账户水平介于上述两者之间，则无需在现金账户与保证金账户之间进行转账。
$$
margin\_account_{0}=|value{0}| \times mr
$$

$$
margin\_account_{t}=min(max(|future\_value_{t}| \times mr,margin\_account_{t-1}\\+total\_future\_pnl_{t}-total\_trading\_cost_{t}),|value_{t}| \times mr \times max\_ratio)
$$

**(19) interest_fee**

​	现金账户利息收益：负的cash_account代表存在着资金挪用或者资金拆解，所以会得到正的利息费用；反之，如果cash_account为正，可以投资银行间隔夜拆解市场，赚取利息收益，则利息费用为负。
$$
interest\_fee_{t}=-cash\_account_{t-1} \times ir/365
$$
**(20) delta_nav**

​	净值变动：每期净值的变动都仅由股指期货损益、交易成本和利息费用构成。
$$
\Delta nav_{t}=total\_pnl_{t}-total\_trading_cost_{t}-interest\_fee_{t}
$$
**(21) nav**

​	资产净值：每期资产净值的存量。
$$
nav_{t}=\Sigma_{i=0}^t\Delta nav_{i}
$$
**(22) cash_account**

​	现金账户数额：现金账户在第一期开仓时，用于缴纳交易手续费；在后续期时，作为margin_account设定值的补足水平的配平项。
$$
cash\_account_{t}=nav_{t}-margin\_account_{t}
$$

------

## 三、对冲策略介绍

对冲策略分为两个维度：月合约权重维度和delta对冲敞口维度。下面介绍相应策略及计算方法：

**（一）月合约权重维度**

**(1) Dominant**

​	主连合约策略：只用持仓量最大的月合约动态对冲，每日主连合约权重为1，其余合约权重为0。

**(2) Current_Month**

​	当月合约策略：只用当月合约动态对冲，每日当月合约权重为1，其余合约权重为0。

**(3) Next_Month**

​	下月合约策略：只用下月合约动态对冲，每日下月合约权重为1，其余合约权重为0。

**(4) Current_Season**

​	当季合约策略：只用当季合约动态对冲，每日当季合约权重为1，其余合约权重为0。

**(5) Next_Season**

​	下季合约策略：只用下季合约动态对冲，每日下季合约权重为1，其余合约权重为0。

**(6) Holding_Weighted**

​	持仓量加权策略：使用持仓量作为当月、下月、当季、下季四个合约的权重进行动态对冲。

**(7) Volume_Weighted**

​	成交量加权策略：使用成交量作为当月、下月、当季、下季四个合约的权重进行动态对冲。

**（二）delta对冲敞口维度**

**(1) HedgeAll**

​	对冲全部的Delta敞口

**(2) HedgeHalf**

​	对冲一半的Delta敞口

**(3) WW_hedge**

​	按照Whalley-Wilmott方法构建delta对冲带

- 当持有期货的delta在对冲带内时，不进行对冲

- 当持有期货的delta突破对冲带上界，则调整头寸使delta等于对冲带上界

- 当持有期货的delta突破对冲带下界，则调整头寸使delta等于对冲带下界

- WW对冲带：$\Delta=\frac{\partial V}{\partial S}±H_0,H_0 =(\frac{3}{2}\frac{ e^{-rT} \lambda S \Gamma^2}{γ})^{1/3} $

  其中$\gamma$为风险厌恶系数，模型默认为1，$\lambda =\frac{tradingcost}{NS}$为按比例计算的交易成本，模型默认为0.005，N为证券交易的总数量。

  若期权有不同到期日，以距离到期日最短的期权的$T$计算$H_0$参数。

**(4) Zakamouline**

按照Zakamouline方法构建delta对冲带

- 当持有期货的delta在对冲带内时，不进行对冲

- 当持有期货的delta突破对冲带上界，则调整头寸使delta等于对冲带上界

- 当持有期货的delta突破对冲带下界，则调整头寸使delta等于对冲带下界

- Zakamouline对冲带：$\Delta=\frac{\partial V(\sigma_m)}{\partial S}±(H_0+H_1),H_0 =\frac{\lambda}{γS\sigma^2T},H_1 = 1.12\lambda^{0.31}T^{0.05}(\frac{e^{-rT}}{\sigma})^{0.25}(\frac{\abs{\Gamma}}{\gamma})^{0.5}$

  其中，$\sigma_m = \sigma \sqrt{1+K}, K=-4.76\frac{\lambda^{0.78}}{T^{0.02}}(\frac{e^{-rT}}{\sigma})^{0.25}(\gamma S^2 \abs{\Gamma})^{0.15}$

  ​			$\gamma$为风险厌恶系数，模型默认为1，

  ​			$\lambda =\frac{tradingcost}{NS}$为按比例计算的交易成本，模型默认为0.005，N为证券交易的总数量。

​	在计算期权组合的Zakamouline对冲带时：

1. 先分别计算构成组合的每个期权的$\sigma_m$和$ \Delta_{im} =\frac{\partial V(\sigma_m)}{\partial S}$ ，
2. 将各个期权调整后的$\Delta_{im}$ 求和得期权组合的$\Delta_{m} = \sum_i \Delta_{im}$
3. 若期权有不同到期日，以距离到期日最短的期权的$T$计算$H_1,H_0,K$等参数。

------

## 四、对冲回测分析框架

对于构建的期权组合数据及相应的对冲策略，进行对冲回测后输出一份可视化Report，Report包含图片如下：

(1) 期权收益分解折线图

(2) 期货持仓与股指点位分析折线图

(3) 股指与股指期货头寸分析折线图

(4) 交易成本拆解分析（除以名义本金）堆叠图

​	动态对冲交易成本/名义本金、展期交易成本/名义本金

(5) 期货对冲端收益拆解分析折线图

​	整体收益/名义本金、期权端收益/名义本金、指数收益/名义本金、基差收益/名义本金、交易成本/名义本金

(6) 期货端收益/名义本金频数分布直方图

(7) 期权端收益/名义本金频数分布直方图

(8) 指数收益/名义本金频数分布直方图

(9) 基差收益/名义本金频数分布直方图

(10) 交易成本/名义本金频数分布直方图

(11) 保证金账户和现金账户序列分析折线图

(12) 保证金账户资金频数分布直方图

(13) 现金账户频数分布直方图

(14) 现金账户隐含资金成本序列折线图

(15) 现金账户隐含资金成本/名义本金频数分布直方图
