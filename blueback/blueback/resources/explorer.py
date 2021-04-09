import os

SECRET_KEY = os.environ.get("ENV_FILE_LOCATION")
print(SECRET_KEY)