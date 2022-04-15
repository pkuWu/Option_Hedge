""" 
@Time    : 2021/12/27 23:11
@Author  : Carl
@File    : cleanData.py
@Software: PyCharm
"""
import pandas as pd
import numpy as np
import pickle5 as pickle

df_all = pd.read_pickle('./data/python_data/2019_2021_mktdata.pkl')

def dataTransform(df_all, col):
    df_transform = df_all[['s_info_windcode', 'trade_dt', col]].copy(deep=False)
    df_transform.set_index(['trade_dt', 's_info_windcode'], inplace=True)
    return df_transform[col].unstack('s_info_windcode')

df_open = dataTransform(df_all, 's_dq_open')
df_close = dataTransform(df_all, 's_dq_close')
df_adjfactor = dataTransform(df_all, 's_dq_adjfactor')
stock_codes = list(set(df_all.s_info_windcode))
trade_dates = list(set(df_all.trade_dt))

from classes.dataDownloader.DataDownloader import DataDownloader
d = DataDownloader()
df_stockInfo = d.read_A_stockInfo()

df_stockInfo_new = df_stockInfo.loc[df_stockInfo.s_info_windcode.isin(stock_codes), ['s_info_windcode', 's_info_listdate', 's_info_delistdate']].copy(deep=False)
df_stockInfo_new.set_index('s_info_windcode', inplace=True)
list_date = df_stockInfo_new.s_info_listdate.to_dict()
delist_date = df_stockInfo_new.s_info_delistdate.to_dict()

basic_data = dict()
basic_data['trade_dates'] = trade_dates
basic_data['stock_codes'] = stock_codes
basic_data['open'] = df_open
basic_data['close'] = df_close
basic_data['adjfactor'] = df_adjfactor
basic_data['list_date'] = list_date
basic_data['delist_date'] = delist_date

with open('./data/cleandata.pkl', 'wb') as file:
    pickle.dump(basic_data, file, protocol=pickle.HIGHEST_PROTOCOL)



