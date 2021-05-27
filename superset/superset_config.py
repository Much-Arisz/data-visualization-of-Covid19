import os 
from cachelib.redis import RedisCache

ROW_LIMIT = 5000
SUPERSET_WORKERS = 4
CSRF_ENABLED = True
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')
CACHE_DEFAULT_TIMEOUT = 86400
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://redis:6379/1'}
SQLALCHEMY_DATABASE_URI = 'mysql://superset:superset@mysql:3306/superset?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisISaSECRET_1234'

class CeleryConfig(object):
    BROKER_URL = 'redis://localhost:6379/1'
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    CELERYD_LOG_LEVEL = 'DEBUG'
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = True

CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
    host='localhost',
    port=6379,
    key_prefix='superset_results'
)

