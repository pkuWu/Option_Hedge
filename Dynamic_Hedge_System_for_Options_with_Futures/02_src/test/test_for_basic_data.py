from classes.basicData.basicData import BasicData
all_trade_dates = BasicData.ALL_TRADE_DATES # 获取所有交易日
price_dict = BasicData.PRICE_DICT # 获取开盘价和收盘价

IF = BasicData.IF_DATA # 获取沪深300数据
IF_close_price = IF['close'] # 将沪深300的收盘价赋值给变量