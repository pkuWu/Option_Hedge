import pickle
class BasicData:
    with open('./data/python_data/cleandata.pkl', 'rb') as file:
        basicData = pickle.load(file)
    # 这里要把基础数据读入
    def __new__(cls):
        return cls
