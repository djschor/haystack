import os
print(os.getcwd())
import pickle
import tempfile
import pytest
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# USER _____________
@pytest.fixture(scope='module')
def new_test_user():
    item = {
        "first_name":"Bart",
        "last_name":"Booty",
        "password": "booty11",
        "phone_number":"7343553625",
        "email":"bbooty@gmail.com",
    }
    return item


# ACCOUNTS _____________________
@pytest.fixture(scope='module')
def new_test_account():
    email = "test@gmail.com"
    item = {
        "account_id":"123",
        "name":"testAcc",
        "official_name": "Official Name",
        "type":"Invest",
        "subtype":"IRA",
        "holdings":"",
        "investment_transactions" :""
    }
    return email, item

@pytest.fixture(scope='module')
def transactions_test_obj():
    tr_f = open('/Users/dschorin/Documents/projects/PersonalFinance/bluechip/pickles/transactions_test_obj.pkl', 'rb')
    tr_obj = pickle.load(tr_f)
    tr_f.close()
    return tr_obj

@pytest.fixture(scope='module')
def holdings_test_obj():
    hg_f = open('/Users/dschorin/Documents/projects/PersonalFinance/bluechip/pickles/holdings_test_obj.pkl', 'rb')
    hg_obj = pickle.load(hg_f)
    hg_f.close()
    return hg_obj

# @pytest.fixture
# def app():
#     """Create and configure a new app instance for each test."""
#     # create a temporary file to isolate the database for each test
#     app = create_app({"TESTING": True, "DATABASE": db_path})

#     # create the database and load test data
#     with app.app_context():
#         init_db()
#         get_db().executescript(_data_sqld)

#     yield app

#     # close and remove the temporary database
#     os.close(db_fd)
#     os.unlink(db_path)


# @pytest.fixture
# def client(app):
#     """A test client for the app."""
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     """A test runner for the app's Click commands."""
#     return app.test_cli_runner()


# class AuthActions(object):
#     def __init__(self, client):
#         self._client = client

#     def login(self, username="test", password="test"):
#         return self._client.post(
#             "/auth/login", data={"username": username, "password": password}
#         )

#     def logout(self):
#         return self._client.get("/auth/logout")


# @pytest.fixture
# def auth(client):
#     return AuthActions(client)