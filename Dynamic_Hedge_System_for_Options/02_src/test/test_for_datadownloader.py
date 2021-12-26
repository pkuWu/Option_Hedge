from classes.dataDownloader.DataDownloader import DataDownloader
d = DataDownloader()
df_result = d.read_A_mktdata(['600000.SH'], 20210101, 20211225)
print(df_result)
