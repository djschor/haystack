# from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_restful import Api
# import os 
# print(os.getcwd())
# from resources.routes import initialize_routes
# from flask_cors import CORS

# app = Flask(__name__)
# app.config.from_envvar('ENV_FILE_LOCATION')
# #app.config.from_envvar('JWT_SECRET_KEY')

# api = Api(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# initialize_routes(api)
# CORS(app)

# app.run(debug=True)