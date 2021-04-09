from flask import Response, request, jsonify
from flask_restful import Resource
import datetime
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import generate_password_hash, check_password_hash

from cacheback.models.userModel import retrieve_user, create_user
from cacheback.models.accountModel import retrieve_accounts_by_type
from cacheback.resources.plaid.backend import get_transactions, get_balance, get_access_token

class SignupApi(Resource):
    def post(self):
        body = request.get_json()

        # check if user exists
        #user = retrieve_user(body['email'])
        user = ''
        if not user: 

            # hash the password
            password = generate_password_hash(body['password']).decode('utf-8')

            # save the user to db
            email = body['email']
            first_name = body['firstname']
            last_name = body['lastname']
            phone = body['mobile']
            user_resp = create_user(email, first_name, last_name, password, phone)
            print(user_resp)
            return {'Result': user_resp}, 200
        # else return duplicate user error

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        # get user 
        user = retrieve_user(body['email'])
        # check password
        authorized = check_password_hash(user['Password'], body['password'])
        print(authorized)
        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user['Email']), expires_delta=expires)
        print(access_token, '\nEND LOGIN')
        return {'token': access_token}, 200
    
class NavApi(Resource):
    def get(self):
        nav = user_nav()
        return nav, 200

class LogoutApi(Resource):
    def post(self): 
        return 'Logout Successful', 200


class InfoApi(Resource):
    @jwt_required
    def get(self):
        print('GETINFO BEGINNING: ')
        current_user = get_jwt_identity()
        print('CURRENT USER TOKEN-> EMAIL: ', current_user)
        user_obj = retrieve_user(current_user)
        print(' USER oBJ: ', user_obj, 'end user oBJ')
        role_ob = role_object('admin')
        return user_obj, 200

import json
class Test(Resource):
    @jwt_required
    def get(self):
        # accountsInfo
        pub_tok = request.args.get('public_token')
        print(pub_tok)
        current_user = get_jwt_identity()
        print(current_user)
        #expense_accounts = retrieve_accounts_by_type(current_user, 'Bank')
        transactions = get_transactions('access-development-a74b8fff-dbf7-415b-8b1e-3a03d34fd7b5', '3JNVEoRvKjS9nadwmoEwCRPD9bnRMJHoPPkay')
        #access = get_access_token(pub_tok)
        #sprint(transactions)
        return transactions, 200

def hash_password(password):
    self.password = generate_password_hash(password).decode('utf8')

def check_password(password):
    return check_password_hash(password)


def role_object(role): 
    if role == 'admin': 
        roleObj = {
            'id': 'admin',
            'name': 'administrator',
            'describe': 'Have all permissions',
            'status': 1,
            'creatorId': 'system',
            'createTime': 1497160610259,
            'deleted': 0,
            'permissions': [{
            'roleId': 'admin',
            'permissionId': 'dashboard',
            'permissionName': 'dashboard',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'query',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'exception',
            'permissionName': 'Exception page permissions',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'Query',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'result',
            'permissionName': 'Result',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"新增"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'Query',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'profile',
            'permissionName': 'Profile',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"Import"},{"action":"get","defaultCheck":False,"describe":"Details"},{"action":"update","defaultCheck":False,"describe":"Update"},{"action":"delete","defaultCheck":False,"describe":"Delete"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'Query',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'table',
            'permissionName': 'Table',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"import","defaultCheck":False,"describe":"Import"},{"action":"get","defaultCheck":False,"describe":"Details"},{"action":"update","defaultCheck":False,"describe":"Update"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'import',
                'describe': 'Import',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'form',
            'permissionName': 'Form Permissions',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"get","defaultCheck":False,"describe":"Details"},{"action":"query","defaultCheck":False,"describe":"Query"},{"action":"update","defaultCheck":False,"describe":"Update"},{"action":"delete","defaultCheck":False,"describe":"Delete"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'Query',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'order',
            'permissionName': 'Order Management',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"新增"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'Query',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'permission',
            'permissionName': 'Admin Permissions',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"get","defaultCheck":False,"describe":"Get"},{"action":"update","defaultCheck":False,"describe":"Update"},{"action":"delete","defaultCheck":False,"describe":"Delete"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'role',
            'permissionName': 'Role Management',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"get","defaultCheck":False,"describe":"Get"},{"action":"update","defaultCheck":False,"describe":"Update"},{"action":"delete","defaultCheck":False,"describe":"Delete"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'table',
            'permissionName': 'Table management',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"新增"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'query',
                'describe': 'Query',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }, {
            'roleId': 'admin',
            'permissionId': 'user',
            'permissionName': 'User Permissions',
            'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"import","defaultCheck":False,"describe":"Import"},{"action":"get","defaultCheck":False,"describe":"Get"},{"action":"update","defaultCheck":False,"describe":"Update"},{"action":"delete","defaultCheck":False,"describe":"Delete"},{"action":"export","defaultCheck":False,"describe":"Export"}]',
            'actionEntitySet': [{
                'action': 'add',
                'describe': 'Add',
                'defaultCheck': False
            }, {
                'action': 'import',
                'describe': 'Import',
                'defaultCheck': False
            }, {
                'action': 'get',
                'describe': 'Get',
                'defaultCheck': False
            }, {
                'action': 'update',
                'describe': 'Update',
                'defaultCheck': False
            }, {
                'action': 'delete',
                'describe': 'Delete',
                'defaultCheck': False
            }, {
                'action': 'export',
                'describe': 'Export',
                'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }]
        }
        permies = roleObj['permissions']
        permies.append(
            {
            'roleId': 'admin',
            'permissionId': 'support',
            'permissionName': 'Support',
            'actions': '[{"action":"add","defaultCheck":false,"describe":"新增"},{"action":"import","defaultCheck":false,"describe":"导入"},{"action":"get","defaultCheck":false,"describe":"详情"},{"action":"update","defaultCheck":false,"describe":"修改"},{"action":"delete","defaultCheck":false,"describe":"删除"},{"action":"export","defaultCheck":false,"describe":"导出"}]',
            'actionEntitySet': [{
            'action': 'add',
            'describe': 'Add',
            'defaultCheck': False
            }, {
            'action': 'import',
            'describe': 'Import',
            'defaultCheck': False
            }, {
            'action': 'get',
            'describe': 'Get',
            'defaultCheck': False
            }, {
            'action': 'update',
            'describe': 'Update',
            'defaultCheck': False
            }, {
            'action': 'delete',
            'describe': 'Delete',
            'defaultCheck': False
            }, {
            'action': 'export',
            'describe': 'Export',
            'defaultCheck': False
            }],
            'actionList': None,
            'dataAccess': None
            }
        )

        roleObj['permissions'] = permies
        return roleObj

def user_nav(): 
    nav = [
        # dashboard
        {
        'name': 'dashboard',
        'parentId': 0,
        'id': 1,
        'meta': {
            'icon': 'dashboard',
            'title': 'Dashboard',
            'show': True
        },
        'component': 'RouteView',
        'redirect': '/dashboard/workplace'
        },
        {
        'name': 'workplace',
        'parentId': 1,
        'id': 7,
        'meta': {
            'title': 'Workplace',
            'show': True
        },
        'component': 'Workplace'
        },
        {
        'name': 'monitor',
        'path': 'https:# www.baidu.com/',
        'parentId': 1,
        'id': 3,
        'meta': {
            'title': 'Monitor',
            'target': '_blank',
            'show': True
        }
        },
        {
        'name': 'Analysis',
        'parentId': 1,
        'id': 2,
        'meta': {
            'title': 'Analysis',
            'show': True
        },
        'component': 'Analysis',
        'path': '/dashboard/analysis'
        },

        # form
        {
        'name': 'form',
        'parentId': 0,
        'id': 10,
        'meta': {
            'icon': 'form',
            'title': 'form'
        },
        'redirect': '/form/base-form',
        'component': 'PageView'
        },
        {
        'name': 'basic-form',
        'parentId': 10,
        'id': 6,
        'meta': {
            'title': '基础表单'
        },
        'component': 'BasicForm'
        },
        {
        'name': 'step-form',
        'parentId': 10,
        'id': 5,
        'meta': {
            'title': 'step-form'
        },
        'component': 'StepForm'
        },
        {
        'name': 'advanced-form',
        'parentId': 10,
        'id': 4,
        'meta': {
            'title': 'Advanced Form'
        },
        'component': 'AdvanceForm'
        },

        # list
        {
        'name': 'list',
        'parentId': 0,
        'id': 10010,
        'meta': {
            'icon': 'table',
            'title': 'table',
            'show': True
        },
        'redirect': '/list/table-list',
        'component': 'PageView'
        },
        {
        'name': 'table-list',
        'parentId': 10010,
        'id': 10011,
        'path': '/list/table-list/:pageNo([1-9]\\d*)?',
        'meta': {
            'title': 'TableList',
            'show': True
        },
        'component': 'TableList'
        },
        {
        'name': 'basic-list',
        'parentId': 10010,
        'id': 10012,
        'meta': {
            'title': 'StandardList',
            'show': True
        },
        'component': 'StandardList'
        },
        {
        'name': 'card',
        'parentId': 10010,
        'id': 10013,
        'meta': {
            'title': 'CardList',
            'show': True
        },
        'component': 'CardList'
        },
        {
        'name': 'search',
        'parentId': 10010,
        'id': 10014,
        'meta': {
            'title': 'Search',
            'show': True
        },
        'redirect': '/list/search/article',
        'component': 'SearchLayout'
        },
        {
        'name': 'article',
        'parentId': 10014,
        'id': 10015,
        'meta': {
            'title': 'SearchArticles',
            'show': True
        },
        'component': 'SearchArticles'
        },
        {
        'name': 'project',
        'parentId': 10014,
        'id': 10016,
        'meta': {
            'title': 'SearchProjects',
            'show': True
        },
        'component': 'SearchProjects'
        },
        {
        'name': 'application',
        'parentId': 10014,
        'id': 10017,
        'meta': {
            'title': 'SearchApplications',
            'show': True
        },
        'component': 'SearchApplications'
        },

        #  profile
        {
        'name': 'profile',
        'parentId': 0,
        'id': 10018,
        'meta': {
            'title': 'profile',
            'icon': 'profile',
            'show': True
        },
        'redirect': '/profile/basic',
        'component': 'RouteView'
        },
        {
        'name': 'basic',
        'parentId': 10018,
        'id': 10019,
        'meta': {
            'title': 'ProfileBasic',
            'show': True
        },
        'component': 'ProfileBasic'
        },
        {
        'name': 'advanced',
        'parentId': 10018,
        'id': 10020,
        'meta': {
            'title': 'ProfileAdvanced',
            'show': True
        },
        'component': 'ProfileAdvanced'
        },

        #  result
        {
        'name': 'result',
        'parentId': 0,
        'id': 10021,
        'meta': {
            'title': 'PageView',
            'icon': 'check-circle-o',
            'show': True
        },
        'redirect': '/result/success',
        'component': 'PageView'
        },
        {
        'name': 'success',
        'parentId': 10021,
        'id': 10022,
        'meta': {
            'title': 'ResultSuccess',
            'hiddenHeaderContent': True,
            'show': True
        },
        'component': 'ResultSuccess'
        },
        {
        'name': 'fail',
        'parentId': 10021,
        'id': 10023,
        'meta': {
            'title': 'ResultFail',
            'hiddenHeaderContent': True,
            'show': True
        },
        'component': 'ResultFail'
        },

        #  Exception
        {
        'name': 'exception',
        'parentId': 0,
        'id': 10024,
        'meta': {
            'title': 'exception',
            'icon': 'warning',
            'show': True
        },
        'redirect': '/exception/403',
        'component': 'RouteView'
        },
        {
        'name': '403',
        'parentId': 10024,
        'id': 10025,
        'meta': {
            'title': '403',
            'show': True
        },
        'component': 'Exception403'
        },
        {
        'name': '404',
        'parentId': 10024,
        'id': 10026,
        'meta': {
            'title': '404',
            'show': True
        },
        'component': 'Exception404'
        },
        {
        'name': '500',
        'parentId': 10024,
        'id': 10027,
        'meta': {
            'title': '500',
            'show': True
        },
        'component': 'Exception500'
        },

        #  account
        {
        'name': 'account',
        'parentId': 0,
        'id': 10028,
        'meta': {
            'title': 'RouteView',
            'icon': 'user',
            'show': True
        },
        'redirect': '/account/center',
        'component': 'RouteView'
        },
        {
        'name': 'center',
        'parentId': 10028,
        'id': 10029,
        'meta': {
            'title': 'AccountCenter',
            'show': True
        },
        'component': 'AccountCenter'
        },
        #  Three Level Menu
        {
        'name': 'settings',
        'parentId': 10028,
        'id': 10030,
        'meta': {
            'title': 'AccountSettings',
            'hideHeader': True,
            'hideChildren': True,
            'show': True
        },
        'redirect': '/account/settings/base',
        'component': 'AccountSettings'
        },
        {
        'name': 'BaseSettings',
        'path': '/account/settings/base',
        'parentId': 10030,
        'id': 10031,
        'meta': {
            'title': 'Base Settings',
            'show': False
        },
        'component': 'BaseSettings'
        },
        {
        'name': 'SecuritySettings',
        'path': '/account/settings/security',
        'parentId': 10030,
        'id': 10032,
        'meta': {
            'title': 'SecuritySettings',
            'show': False
        },
        'component': 'SecuritySettings'
        },
        {
        'name': 'CustomSettings',
        'path': '/account/settings/custom',
        'parentId': 10030,
        'id': 10033,
        'meta': {
            'title': 'CustomSettings',
            'show': False
        },
        'component': 'CustomSettings'
        },
        {
        'name': 'BindingSettings',
        'path': '/account/settings/binding',
        'parentId': 10030,
        'id': 10034,
        'meta': {
            'title': 'BindingSettings',
            'show': False
        },
        'component': 'BindingSettings'
        },
        {
        'name': 'NotificationSettings',
        'path': '/account/settings/notification',
        'parentId': 10030,
        'id': 10034,
        'meta': {
            'title': 'NotificationSettings',
            'show': False
        },
        'component': 'NotificationSettings'
        }
    ]
    return nav