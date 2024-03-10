import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(ROOT_DIR, 'database')

SQLITE_DIR = os.path.join(DATABASE_DIR, 'despensa_sqlite')
POSTGRES_DIR = os.path.join(DATABASE_DIR, 'despensa_postgres')

ENVIRONMENT_VARIABLE_NAME = 'DESPENSA_ENV'
TEST = 'test'
MAIN = 'main'

SQLITE_DEV_DB = os.path.join(SQLITE_DIR, 'despensa.sqlite')
SQLITE_TEST_DB = os.path.join(SQLITE_DIR, 'despensa_test.sqlite')
SQLITE_SAMPLE_DATA = os.path.join(SQLITE_DIR, 'sample_data.sql')
SQLITE_CREATE_TABLES = os.path.join(SQLITE_DIR, 'create_tables.sql')
SQLITE_DROP_TABLES = os.path.join(SQLITE_DIR, 'drop_tables.sql')

POSTGRES_CREATE_TABLES = os.path.join(POSTGRES_DIR, 'create_tables.sql')
POSTGRES_DROP_TABLES = os.path.join(POSTGRES_DIR, 'drop_tables.sql')
POSTGRES_SAMPLE_DATA = os.path.join(POSTGRES_DIR, 'sample_data.sql')

POSTGRES = 2
SQLITE = 3
