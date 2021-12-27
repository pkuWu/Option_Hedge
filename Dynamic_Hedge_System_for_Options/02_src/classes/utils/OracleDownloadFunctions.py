# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 10:35:28 2021

@author: Hejinze
"""
import cx_Oracle as cx
import pandas as pd
import re
from tqdm import tqdm
class SqlDownloader:
    def __init__(self, user_name='student1901212582', password='student1901212582',
                 database_location='219.223.208.52:1521/orcl'):
        self.user_name = user_name
        self.password = password
        self.database_location = database_location
        self.login()
        
    def login(self):
        self.conn = cx.connect(self.user_name,self.password,self.database_location)
        self.cursor = self.conn.cursor()
        
    def fetch_huge_data_from_sql(self, sql):
        splitted_sqls = self.split_sql(sql)
        column_names = self.get_columns_from_sql(sql)
        if len(splitted_sqls)>1:
            sql_data_list = []
            for i,t_sql in tqdm(enumerate(splitted_sqls)):
                temp_data = pd.DataFrame(self.get_single_data_from_sql(t_sql), 
                                         columns = column_names)
                sql_data_list.append(temp_data)
            return pd.concat(sql_data_list, axis=0, ignore_index=True)
        else:
            temp_data = pd.DataFrame(self.get_single_data_from_sql(splitted_sqls[0]), 
                                         columns = column_names)
            return temp_data
    
    def get_single_data_from_sql(self, sql):
        self.cursor.execute(sql)
        temp_data = self.cursor.fetchall()
        return temp_data
    
    @staticmethod
    def get_columns_from_sql(sql):
        return re.findall('select\n\s*(.*?)\n\s*from',sql)[0].strip().split(',')
    
    @staticmethod
    def parse_sql(sql):
        column_names = SqlDownloader.get_columns_from_sql(sql)
        table_name = re.findall('from\n\s*(.*?)\n\s*where',sql)[0]
        date_column_name,start_date = re.findall('\n\s*(.*)>=\'(\d\d\d\d\d\d\d\d)\'',sql)[0]
        date_column_name,end_date = re.findall('\n\s*(.*)<=\'(\d\d\d\d\d\d\d\d)\'',sql)[0]
        other_conditions = re.findall('\n\s*(.*[^><]=.*)',sql)
        order_info = re.findall('(order by\n\s*.*\n)',sql)
        # in_column_name, in_range = re.findall('\n\s*(.*)\sin\s(\(\'.*\'\))',sql)[0]
        reg_info = re.findall('\s(regexp_like\(.*?\))\n',sql)
        sql_info_dict = {'column_names':column_names, 'table_name':table_name,
                         'date_column_name':date_column_name, 'start_date':start_date,
                         'end_date':end_date, 'other_conditions':other_conditions,
                         'order_info':order_info,'reg_info':reg_info}
        return sql_info_dict
    
    @staticmethod
    def split_sql(sql):
        sql_info_dict = SqlDownloader.parse_sql(sql)
        time_points = generate_time_points(sql_info_dict['start_date'], sql_info_dict['end_date'])
        sql_list = []
        for start_date, end_date in time_points:
            temp_sql = SqlDownloader.generate_sql(sql_info_dict, start_date, end_date)
            sql_list.append(temp_sql)
        return sql_list
    
    @staticmethod
    def generate_sql(sql_info_dict, start_date, end_date):
        output_sql = 'select\n'
        output_sql = output_sql+'    {}\nfrom\n'.format(','.join(sql_info_dict['column_names']))
        output_sql = output_sql+'    {}\nwhere\n'.format(sql_info_dict['table_name'])
        output_sql = output_sql+'''    {0:s}>='{1:s}'\nand\n'''.format(sql_info_dict['date_column_name'],start_date)
        output_sql = output_sql+'''    {0:s}<='{1:s}'\n'''.format(sql_info_dict['date_column_name'],end_date)
        if len(sql_info_dict['other_conditions'])>0:
            output_sql = output_sql+'and\n    '+'\nand\n    '.join(sql_info_dict['other_conditions'])+'\n'
        if len(sql_info_dict['order_info'])>0:
            output_sql = output_sql+sql_info_dict['order_info'][0]
        return output_sql

def cal_yyyyQn(date):
    if date[4:6]<='03':
        return date[0:4]+'Q1'
    if date[4:6]<='06':
        return date[0:4]+'Q2'
    if date[4:6]<='09':
        return date[0:4]+'Q3'
    return date[0:4]+'Q4'

def first_date_ofQ(yyyyQn):
    year = yyyyQn[0:4]
    n = int(yyyyQn[-1])
    if n==1:
        return year+'0101'
    if n==2:
        return year+'0401'
    if n==3:
        return year+'0701'
    return year+'1001'
        
def last_date_ofQ(yyyyQn):
    year = yyyyQn[0:4]
    n = int(yyyyQn[-1])
    if n==1:
        return year+'0331'
    if n==2:
        return year+'0630'
    if n==3:
        return year+'0930'
    return year+'1231'

def floor_date(date):
    return first_date_ofQ(cal_yyyyQn(date))

def ceil_date(date):
    return last_date_ofQ(cal_yyyyQn(date))

def next_Q(yyyyQn):
    year = yyyyQn[0:4]
    n = int(yyyyQn[-1])
    if n<4:
        return year+'Q{0:d}'.format(n+1)
    return str(int(year)+1)+'Q1'

def generate_time_points(start_date, end_date):
    assert cal_yyyyQn(start_date)<=cal_yyyyQn(end_date), 'start_date must be ahead of end_date'
    if cal_yyyyQn(start_date)==cal_yyyyQn(end_date):
        return (start_date,end_date)
    time_points = [(start_date, last_date_ofQ(cal_yyyyQn(start_date)))]
    curr_Q = cal_yyyyQn(start_date)
    while next_Q(curr_Q)<cal_yyyyQn(end_date):
        curr_Q = next_Q(curr_Q)
        time_points.append((first_date_ofQ(curr_Q),last_date_ofQ(curr_Q)))
    curr_Q = next_Q(curr_Q)
    time_points.append((first_date_ofQ(curr_Q),end_date))
    return time_points

def tuples_to_list(list_of_tuples):
    return [x[0] for x in list_of_tuples]

def tuples_to_dataframe(list_of_tuples):
    return pd.DataFrame(list_of_tuples)
if __name__ == '__main__':
    tt = generate_time_points('20201002','20210228')
    tt = generate_time_points('20120301','20120431')
    tt = generate_time_points('20111111','20120105')
    tt = generate_time_points('20120227','20120305')
