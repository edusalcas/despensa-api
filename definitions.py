import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(ROOT_DIR, 'despensa')
TEST_DIR = os.path.join(ROOT_DIR, 'tests')

ENVIRONMENT_VARIABLE_NAME = 'DESPENSA_ENV'
TEST = 'test'
MAIN = 'main'

SQLITE_DB = 'database/despensa.sqlite'
SQLITE_SAMPLE_DATA = 'database/sample_data.sql'

