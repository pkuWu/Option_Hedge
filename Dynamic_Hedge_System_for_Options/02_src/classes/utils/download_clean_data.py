from OracleDownloadFunctions import SqlDownloader
import pickle
sdl = SqlDownloader()
t_sql = '''
            select
                S_INFO_WINDCODE, TRADE_DT, S_DQ_OPEN, S_DQ_CLOSE, S_DQ_ADJFACTOR
            from
                FILESYNC.AshareEODPrices
            where
                regexp_like(S_INFO_WINDCODE,'^[0-9]......S.')
            and
                TRADE_DT>='20190101'
            and
                TRADE_DT<='20211227'
'''
temp_data = sdl.fetch_huge_data_from_sql(t_sql)
with open('stock_data.pickle','wb+') as f:
    pickle.dump(temp_data,f)
