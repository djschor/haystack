from .users import UserApi, UsersApi
# from .plaid.backend import Balance, Transactions
from .plaid.frontend import AccessToken, LinkToken, PublicToken
from .stocks import StockApi, StocksApi, FourHourPricing, HourPricing, ThirtyMinutePricing, FifteenMinutePricing, FiveMinutePricing, OneMinutePricing, HistoricalPricing, TimeDataHistorical, TimeSchema
from .accounts import AccountApi
from .auth import RegisterApi, LoginApi, NavApi, LogoutApi, InfoApi, Test
from .ant import CurrentUser, AntUsers, Error500, Error404, Error403, Error401, Captcha, Notices
def initialize_routes(api):
    # USERS
    api.add_resource(UserApi, '/api/user/')
    api.add_resource(UsersApi, '/api/user/users')
    # api.add_resource(CreateUserApi, '/api/user/create/<email>')
  
    # PLAID FRONT
    # api.add_resource(AccessToken, '/api/auth/plaid/access')
    # api.add_resource(LinkToken, '/api/auth/plaid/link')
    api.add_resource(PublicToken, '/api/auth/plaid/public')

    # AUTH
    api.add_resource(RegisterApi, '/api/auth/register')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(LogoutApi, '/api/auth/logout')

    # STOCK
    api.add_resource(StockApi, '/api/stock/<symbol>')
    api.add_resource(StocksApi, '/api/stocks')
    api.add_resource(FourHourPricing, '/api/stock/4hr/<symbol>')
    api.add_resource(HourPricing, '/api/stock/1hr/<symbol>')
    api.add_resource(ThirtyMinutePricing, '/api/stock/30min/<symbol>')
    api.add_resource(FifteenMinutePricing, '/api/stock/15min/<symbol>')
    api.add_resource(FiveMinutePricing, '/api/stock/5min/<symbol>')
    api.add_resource(OneMinutePricing, '/api/stock/1min/<symbol>')
    api.add_resource(HistoricalPricing, '/api/stock/historical/<symbol>')
    api.add_resource(TimeDataHistorical, '/api/stock/historicaldata/<symbol>')
    api.add_resource(TimeSchema, '/api/stock/timeschema')



    # ACCOUNTS
    api.add_resource(AccountApi, '/api/accounts')

    # test
    api.add_resource(Test, '/api/test')

    # ant react
    api.add_resource(CurrentUser, '/api/ant/currentUser')
    api.add_resource(AntUsers, '/api/ant/users')
    api.add_resource(Error500, '/api/500')
    api.add_resource(Error404, '/api/404')
    api.add_resource(Error403, '/api/403')
    api.add_resource(Error401, '/api/401')
    api.add_resource(Captcha, '/api/login/captcha')
    api.add_resource(Notices, '/api/notices')
