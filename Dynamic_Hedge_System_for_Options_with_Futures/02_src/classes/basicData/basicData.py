import pickle

class BasicData:
    with open('./data/python_data/clean_data.pickle', 'rb') as file:
        basic_data = pickle.load(file)

    ALL_TRADE_DATES = basic_data['trade_date']
    PRICE_DICT = dict()
    PRICE_DICT['open'] = basic_data['open']
    PRICE_DICT['close'] = basic_data['close']

    with open('./data/python_data/future_data.pickle', 'rb') as file:
        FUTURE_DATA = pickle.load(file)

    def __new__(cls):
        return cls
