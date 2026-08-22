import os
from dotenv import load_dotenv

load_dotenv()

class UserDataBaseCreds:
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    USERNAME = os.getenv("USERNAME_DB")
    PASSWORD = os.getenv("PASSWORD_DB")
