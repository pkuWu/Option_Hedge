import pickle

class BasicData:
    with open('./data/python_data/cleandata.pkl', 'rb') as file:
        basicData = pickle.load(file)

    PRICE_DICT = dict()
    PRICE_DICT['open'] = basicData['open']
    PRICE_DICT['close'] = basicData['close']
    # 这里要把基础数据读入
    def __new__(cls):
        return cls

