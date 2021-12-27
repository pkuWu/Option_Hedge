from classes.dataDownloader.DataDownloader import DataDownloader
d = DataDownloader()
df_stock = d.read_A_stockInfo()
for i in range(3):
    year = 2019 + i
    bgtdate = int(year * 10000 + 101)
    enddate = int(year * 10000 + 1231)
    df_part = d.read_A_mktdata(bgtdate, enddate, whole=True)
    if i == 0:
        df_result = df_part.copy()
    else:
        df_result.append(df_part.copy())

df_result.to_pickle('./data/Wind_data/2011_2021_mktdata.pk')
print(df_result)
