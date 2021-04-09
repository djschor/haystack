import os
import sys
print('CWD: ',os.getcwd())
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from cacheback.resources.routes import initialize_routes

#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
bcrypt = Bcrypt()
api = Api()
jwt = JWTManager()
cors = CORS()

######################################
#### Application Factory Function ####
######################################
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_envvar('ENV_FILE_LOCATION')
    app.config.from_pyfile('config.py')
    initialize_extensions(app)
    return app

##########################
#### Helper Functions ####
##########################ç
def initialize_extensions(app):
  # Since the application instance is now created, pass it to each Flask
  # extension instance to bind it to the Flask application instance (app)
  initialize_routes(api)
  api.init_app(app)
  bcrypt.init_app(app)
  cors.init_app(app)
  jwt.init_app(app)
  cors.init_app(app)
  
