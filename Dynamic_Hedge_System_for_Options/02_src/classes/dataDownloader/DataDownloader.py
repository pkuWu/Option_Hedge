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


class DataDownloader:
    def __init__(self, ini_file='./classes/dataDownloader/database.ini', section='WIND'):
        self.ini_file = ini_file
        self.section = section
        self.config = self.read_db_config()
        self.eng = sa.create_engine('{dbtype}://{user}:{password}@{host}:{port}/{sid}'.format(**self.config))

    def read_db_config(self):
        if not os.path.exists(self.ini_file):
            raise IOError('不存在服务器参数配置文件[%s]' % self.ini_file)

        config = configparser.ConfigParser()
        config.read(self.ini_file, encoding='utf-8')
        if self.section in config.sections():
            db_config = dict(config._sections[self.section])
        else:
            print('不存在section: ' + self.section)
            db_config = {}
        return db_config

    def read_A_mktdata(self, bgtdate, enddate, stock_list=None, whole=False):

        if not whole:
            if len(stock_list) == 0:
                raise Warning('stock_list cannot be None!')
            elif len(stock_list) == 1:
                stock_list = f'(\'{stock_list[0]}\')'
            else:
                stock_list = tuple(stock_list)

            query = '''
                SELECT S_INFO_WINDCODE, TRADE_DT, S_DQ_OPEN, S_DQ_PRECLOSE, S_DQ_CLOSE, S_DQ_PCTCHANGE, S_DQ_VOLUME, S_DQ_ADJFACTOR
                A_DQ_AVGPRICE, S_DQ_TRADESTATUS
                FROM FILESYNC.AshareEODPrices
                WHERE S_INFO_WINDCODE IN {}
                AND TRADE_DT >= {}
                AND TRADE_DT <= {}
                '''.format(stock_list, bgtdate, enddate)
        else:
            query = '''
                SELECT S_INFO_WINDCODE, TRADE_DT, S_DQ_OPEN, S_DQ_PRECLOSE, S_DQ_CLOSE, S_DQ_PCTCHANGE, S_DQ_VOLUME, S_DQ_ADJFACTOR
                A_DQ_AVGPRICE, S_DQ_TRADESTATUS
                FROM FILESYNC.AshareEODPrices
                WHERE TRADE_DT >= {}
                AND TRADE_DT <= {}
                '''.format(bgtdate, enddate)

        return pd.read_sql(query, self.eng)

    def read_A_stockInfo(self, columns=None):
        if columns is None:
            query = '''
            SELECT * 
            FROM FILESYNC.AShareDescription
            '''
        else:
            _columns = ', '.join(columns)
            query = '''
            SELECT {}
            FROM FILESYNC.AShareDescription
            '''.format(_columns)

        return pd.read_sql(query, self.eng)