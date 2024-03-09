from despensa.abstract_connector import AbstractConnector
from despensa.postgres_connector import PostgresConnector
from despensa.sqlite_connector import SQLiteConnector

from environment import Environment
import definitions as d


class DatabaseConnectorFactory(object):
    @staticmethod
    def get_database_connector() -> AbstractConnector:
        current_database: int = Environment().get_current_database()

        if current_database == d.SQLITE:
            return SQLiteConnector()
        elif current_database == d.POSTGRES:
            return PostgresConnector()
