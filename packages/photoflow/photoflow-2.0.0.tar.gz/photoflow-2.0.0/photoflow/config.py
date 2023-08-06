import os


class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.environ.get("DATABASE")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = os.environ.get("SECRET")
    SECRET_KEY = os.environ.get("SECRET")
    SEND_FILE_MAX_AGE_DEFAULT = 60
    PUBLIC_ON_HOME = os.environ.get("PUBLIC_ON_HOME", "no") == "yes"

    def __init__(self):
        if not os.environ.get("DATABASE"):
            print("DATABASE is not defined")
            exit(1)
