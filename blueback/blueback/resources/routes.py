from .users import UserApi
from .accounts import AccountApi
# from .plaid.backend import Balance, Transactions
from .plaid.frontend import AccessToken, LinkToken, PublicToken
from .auth import SignupApi, LoginApi, NavApi, LogoutApi, InfoApi, Test
def initialize_routes(api):
    # USERS
    api.add_resource(UserApi, '/api/users')
    
    # ACCOUNTS
    api.add_resource(AccountApi, '/api/users/accounts')
    
    # PLAID FRONT
    api.add_resource(AccessToken, '/api/auth/plaid/access')
    api.add_resource(LinkToken, '/api/auth/plaid/link')
    api.add_resource(PublicToken, '/api/auth/plaid/public')

    # AUTH
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(NavApi, '/api/user/nav')
    api.add_resource(LogoutApi, '/api/auth/logout')
    api.add_resource(InfoApi, '/api/user/info')

    # test
    api.add_resource(Test, '/api/test')

