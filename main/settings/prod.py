import os
import dj_database_url

from .base import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
BUILD = 'prod'

DATABASES = {'default': dj_database_url.config()}
# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

CORS_ORIGIN_WHITELIST = (
    'https://www.snippets-app.com',
    'www.snippets-app.com',
    'snippets-app.com',
)

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ['MAILGUN_API_KEY'],
    "MAILGUN_SENDER_DOMAIN": os.environ['MAILGUN_SENDER_DOMAIN'],
}
