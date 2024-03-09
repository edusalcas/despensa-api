import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(ROOT_DIR, 'despensa')
TEST_DIR = os.path.join(ROOT_DIR, 'tests')
POSTGRES_DIR = os.path.join(ROOT_DIR, 'despensa_postgres')


ENVIRONMENT_VARIABLE_NAME = 'DESPENSA_ENV'
TEST = 'test'
MAIN = 'main'

SQLITE_DB = 'database/despensa.sqlite'
SQLITE_SAMPLE_DATA = os.path.join(MAIN_DIR, 'database/sample_data.sql')
SQLITE_CREATE_TABLES = os.path.join(MAIN_DIR, 'database/create_tables.sql')
SQLITE_DROP_TABLES = os.path.join(MAIN_DIR, 'database/drop_tables.sql')

POSTGRES_CREATE_TABLES = os.path.join(POSTGRES_DIR, 'create_tables.sql')
POSTGRES_DROP_TABLES = os.path.join(POSTGRES_DIR, 'drop_tables.sql')
POSTGRES_SAMPLE_DATA = os.path.join(POSTGRES_DIR, 'sample_data.sql')

POSTGRES = 2
SQLITE = 3
