from decouple import config

SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
DEBUG = config('DEBUG', cast=bool)
SQLALCHEMY_TRACK_MODIFICATIONS = False
