import os

#Used by flask to encrypt
SECRET_KEY='secret'

PROJECT_ID = 'processed-videos2'
DATA_BACKEND = 'cloudsql'
CLOUDSQL_USER = 'video_analyzer'
CLOUDSQL_PASSWORD = '497rUlz!'
CLOUDSQL_DATABASE = 'epilepsy_filter'
CLOUDSQL_CONNECTION_NAME = 'epilepsy-video-filter:us-central1:processed-videos2'


LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI