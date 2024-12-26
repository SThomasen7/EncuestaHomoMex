"""Development configuration"""

import pathlib

APPLICATION_ROOT = '/'

SECRET_KEY = b'' ## FIXME
SESSION_COOKIE_NAME = 'login'

HOMOMEX_ROOT = pathlib.Path(__file__).resolve().parent.parent

DATABASE = HOMOMEX_ROOT/'var'/'HomoMex.sqlite3'
