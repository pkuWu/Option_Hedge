import pandas as pd
import pickle

excel_file = '../Wind_data/stock_index_price.xlsx'
all_trade_dates = list(pd.read_excel(excel_file,sheet_name='交易日',squeeze=True))
open_price = pd.read_excel(excel_file,sheet_name='open').set_index('date')
close_price = pd.read_excel(excel_file,sheet_name='close').set_index('date')
data_dict = {'trade_date': all_trade_dates, 'open':open_price,'close':close_price}
with open('../python_data/clean_data.pickle', 'wb+') as f:
    pickle.dump(data_dict,f)

