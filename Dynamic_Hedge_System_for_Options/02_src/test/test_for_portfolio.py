from classes.options.Option_Portfolio import Option_Portfolio

# test for Option_Portfolio
# para_dict1 = {'portfolio_class':'CallSpread',
#              'notional':12e6,
#              'start_date':'20190129',
#              'end_date':'20191231',
#              'K_low':5.42,
#              'K_high':5.98,
#              'option_fee':1780800,
#              'stock_code':'300277.SZ',
#              'start_price':6.19,
#              'position1':1,
#              'position2':-1}
#
# para_dict2 = {'portfolio_class':'PutSpread',
#              'notional':12e6,
#              'start_date':'20190129',
#              'end_date':'20191231',
#              'K_low':5.42,
#              'K_high':5.98,
#              'option_fee':1780800,
#              'stock_code':'300277.SZ',
#              'start_price':6.19,
#              'position1':-1,
#              'position2':1}
#
# option_portfolio = Option_Portfolio()
# option_portfolio.create_portfolio_dict(**para_dict1)
# option_portfolio.calculate_portfolio_greeks()
# portfolio_greeks=option_portfolio.return_result()

# butterFly_paras = {'portfolio_class':'ButterflySpread',
#              'notional':12e6,
#              'start_date':'20190129',
#              'end_date':'20191231',
#              'K_low':5.42,
#              'K_high':5.98,
#              'stock_code':'300277.SZ',
#              'start_price':6.19,
#             }
#
# option_portfolio = Option_Portfolio()
# option_portfolio.create_portfolio_dict(**butterFly_paras)
# option_portfolio.calculate_portfolio_greeks()
# portfolio_greeks=option_portfolio.return_result()

strangle_paras = {'portfolio_class': 'Strangle',
             'notional':12e6,
             'start_date':'20190129',
             'end_date':'20191231',
             'K_low':5.42,
             'K_high':5.98,
             'stock_code':'300277.SZ',
             'start_price':6.19,
            }

option_portfolio = Option_Portfolio()
option_portfolio.create_portfolio_dict(**strangle_paras)
option_portfolio.calculate_portfolio_greeks()
portfolio_greeks=option_portfolio.return_result()
