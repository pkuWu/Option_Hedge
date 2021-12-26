""" 
@Time    : 2021/12/23 20:16
@Author  : Carl
@File    : Data.py
@Software: PyCharm
"""
import pandas as pd
import numpy as np
import cx_Oracle
import sqlalchemy as sa
import os
import configparser

class Data:
    def __init__(self, ini_file='./Data/database.ini', section='WIND'):
        self.ini_file = ini_file
        self.section = section
        self.config = self.read_db_config()
        self.eng = sa.create_engine(('{dbtype}://{user}:{password}@{host}:{port}/{sid}').format(**self.config))

    def read_db_config(self):
        if not os.path.exists(self.ini_file):
            raise IOError('不存在服务器参数配置文件[%s]' % ini_file)

        config = configparser.ConfigParser()
        config.read(self.ini_file, encoding='utf-8')
        db_config = {}
        if self.section in config.sections():
            db_config = dict(config._sections[self.section])
        else:
            print('不存在section: ' + self.section)
        return db_config

    def read_A_mktdata(self, stock_list, bgtdate, enddate):
        if len(stock_list) == 0:
            raise Warning('stock_list cannot be None!')
        elif len(stock_list) == 1:
            stock_list = f'(\'{stock_list[0]}\')'
        else:
            stock_list = tuple(stock_list)

        query = """
        SELECT S_INFO_WINDCODE, TRADE_DT, S_DQ_OPEN, S_DQ_PRECLOSE, S_DQ_CLOSE, S_DQ_PCTCHANGE, S_DQ_VOLUME, S_DQ_ADJFACTOR
        A_DQ_AVGPRICE, S_DQ_TRADESTATUS
        FROM FILESYNC.AshareEODPrices
        WHERE S_INFO_WINDCODE IN {}
        AND TRADE_DT > {}
        AND TRADE_DT < {}
        """.format(stock_list, bgtdate, enddate)

        return pd.read_sql(query, self.eng)

# case
# d = Data()
# df_result = d.read_A_mktdata(['600000.SH'], 20210101, 20211225)
# print(df_result)
