from environment import Environment
from despensa.controller import Controller
from despensa.sqlite_connector import SQLiteConnector

Environment().working_is_test()


class TestSingleton:
    def test_controller_singleton(self):
        c1 = Controller()
        c2 = Controller()
        assert c1 is c2, "Not the same object"

    def test_sqlite_connector_singleton(self):
        sqlite_connector1 = SQLiteConnector()
        sqlite_connector2 = SQLiteConnector()
        assert sqlite_connector1 is sqlite_connector2
