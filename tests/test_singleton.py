from despensa import controller, sqlite_connector

PATH_TEST_DB: str = "tests/database/despensa_test.sqlite"


class TestSingleton:
    def test_controller_singleton(self):
        assert controller.get_unique_instance() is controller.get_unique_instance()

    def test_sqlite_connector_singleton(self):
        assert sqlite_connector.get_unique_instance(database_path=PATH_TEST_DB) is \
               sqlite_connector.get_unique_instance(database_path=PATH_TEST_DB)
