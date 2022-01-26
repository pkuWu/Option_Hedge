import pandas as pd
import pickle

excel_file = '../Wind_data/stock_index_price.xlsx'
all_trade_dates = list(pd.read_excel(excel_file,sheet_name='交易日',squeeze=True))
open_price = pd.read_excel(excel_file,sheet_name='open').set_index('date')
close_price = pd.read_excel(excel_file,sheet_name='close').set_index('date')
data_dict = {'trade_date': all_trade_dates, 'open':open_price,'close':close_price}
with open('../python_data/clean_data.pickle', 'wb+') as f:
    pickle.dump(data_dict,f)

IF_excel_file = '../Wind_data/沪深300股指期货数据.xlsx'
IH_excel_file = '../Wind_data/上证50股指期货数据.xlsx'
IC_excel_file = '../Wind_data/中证500股指期货数据.xlsx'

future_dict = {}
for file in [IF_excel_file, IH_excel_file, IC_excel_file]:
    open_price = pd.read_excel(file, sheet_name='price_open').set_index('date')
    close_price = pd.read_excel(file, sheet_name='price_close').set_index('date')
    holding = pd.read_excel(file, sheet_name='holding').set_index('date')
    volume = pd.read_excel(file, sheet_name='volume').set_index('date')
    month_code = pd.read_excel(file, sheet_name='month_code').set_index('date')
    data_dict = {'open': open_price, 'close': close_price, 'holding': holding, 'volume': volume, 'month_code': month_code}
    if file == IF_excel_file:
        future_dict['IF'] = data_dict
    elif file == IH_excel_file:
        future_dict['IH'] = data_dict
    elif file == IC_excel_file:
        future_dict['IC'] = data_dict
with open('../python_data/future_data.pickle', 'wb+') as f:
    pickle.dump(future_dict, f)