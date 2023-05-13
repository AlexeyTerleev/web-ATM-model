from dotenv import load_dotenv
from os import environ

load_dotenv()


DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_PORT = environ.get("DB_PORT")
DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")

JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = environ.get("JWT_REFRESH_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
