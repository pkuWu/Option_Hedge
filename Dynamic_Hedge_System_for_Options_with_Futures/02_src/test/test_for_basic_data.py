from classes.basicData.basicData import BasicData
all_trade_dates = BasicData.ALL_TRADE_DATES # 获取所有交易日
price_dict = BasicData.PRICE_DICT # 获取开盘价和收盘价

future_data = BasicData.FUTURE_DATA # 获取所有期货数据
IF = BasicData.FUTURE_DATA['IF'] # 获取沪深300股指期货数据
IF_close_price = IF['close'] # 将沪深300的收盘价赋值给变量