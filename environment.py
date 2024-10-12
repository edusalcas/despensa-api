import os
from dataclasses import dataclass

from despensa.singleton_meta import SingletonMeta
import definitions as d


@dataclass
class PostgresConfig(object):
    host: str
    port: int
    user: str
    password: str
    database: str
    create_tables_sql_path: str = d.POSTGRES_CREATE_TABLES
    drop_tables_sql_path: str = d.POSTGRES_DROP_TABLES
    generate_samples_sql_path: str = d.POSTGRES_SAMPLE_DATA


@dataclass
class SQLiteConfig(object):
    db_path: str
    create_tables_sql_path: str = d.SQLITE_CREATE_TABLES
    drop_tables_sql_path: str = d.SQLITE_DROP_TABLES
    generate_samples_sql_path: str = d.SQLITE_SAMPLE_DATA

DEV: int = 0
TEST: int = 1
class Environment(metaclass=SingletonMeta):
    __postgres_config_dev: PostgresConfig = PostgresConfig(
        host='localhost',
        port=5432,
        user='postgres',
        password='despensa_pass',
        database='postgres',
    )

    __postgres_config_test: PostgresConfig = PostgresConfig(
        host='localhost',
        port=5432,
        user='postgres',
        password='despensa_pass',
        database='test',
    )

    __sqlite_config_dev: SQLiteConfig = SQLiteConfig(
        db_path=d.SQLITE_DEV_DB,
    )

    __sqlite_config_test: SQLiteConfig = SQLiteConfig(
        db_path=d.SQLITE_TEST_DB,
    )

    def __init__(self):
        self.__current_env: int = DEV
        self.__use_database: int = d.POSTGRES

    def get_current_env(self):
        return self.__current_env

    def working_is_dev(self):
        self.__current_env = DEV

    def working_is_test(self):
        self.__current_env = TEST

    def get_current_database(self) -> int:
        return self.__use_database

    def set_current_database(self, database: int):
        self.__use_database = database

    def get_postgres_config(self) -> PostgresConfig:
        if self.__current_env == DEV:
            return self.__postgres_config_dev
        elif self.__current_env == TEST:
            return self.__postgres_config_test

    def get_sqlite_config(self) -> SQLiteConfig:
        if self.__current_env == DEV:
            return self.__sqlite_config_dev
        elif self.__current_env == TEST:
            return self.__sqlite_config_test
