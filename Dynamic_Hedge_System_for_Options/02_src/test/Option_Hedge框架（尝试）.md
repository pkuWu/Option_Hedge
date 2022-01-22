# Option_Hedge框架（尝试）

## 1. parameter

```python
# params -> dict
params = {
    option_type: "VanillaCall" #包括vanilla, Barrier, Option_portfolio等
    notional: 
    strat_date:
    end_date:
    stock_code:
    start_price: # 这些参数是所有类型期权共有的，全部有OptionBase里面的set_basic_params()设定
    K:
    H: #这些参数不同种类的期权不同，由OptionBase里面的set_specific_params()方法根据期权种类设定
}
```

## 2. OptionBase

### 实现的功能：

### 1.  为不同种类的期权设定参数：set_basic_params(), set_specific_params()

### 2.  期权收益分解及其可视化

## 3. 期权类（Vanilla, Barrier, OptionPortfolio）

### 实现的功能：

### 计算希腊值

## 4. Backtest

### 实现功能待定