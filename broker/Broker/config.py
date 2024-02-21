from dotenv import load_dotenv
import os

load_dotenv()

AUTHORIZATION_URL = os.environ.get("AUTHORIZATION_URL")
GET_TOKENS_URL = os.environ.get("GET_TOKENS_URL")
POST_ASSET_URL = os.environ.get("POST_ASSET_URL")
POST_OPERATION_URL = os.environ.get("POST_OPERATION_URL")
GET_INSTRUMENT_LIST = os.environ.get("GET_INSTRUMENT_LIST")

SUPER_USER_MAIL = os.environ.get("SUPER_USER_MAIL")
SUPER_USER_PASSWORD = os.environ.get("SUPER_USER_PASSWORD")


DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
DB_USER = os.environ.get("DB_USER")
