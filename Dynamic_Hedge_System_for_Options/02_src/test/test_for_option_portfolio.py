from classes.options.option_portfolio2 import OptionPortfolio

# set parameters
paras = {
    'option_type': 'BullCallSpread',
    'notional': 12e6,
    'start_date': '20190129',
    'end_date': '20191231',
    'K': [5.42, 5.98],
    'stock_code': '300277.SZ',
    'start_price': 6.19
}

option_portfolio = OptionPortfolio()
option_portfolio.get_option_list(paras)
greek_df = option_portfolio.get_greek_df()
decompose_df = option_portfolio.get_return_decomposition()
option_portfolio.decomposition_vis()