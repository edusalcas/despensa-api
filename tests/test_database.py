import pytest

from main.sqlite_connector import get_unique_instance, SQLiteConnector, AlimentTable
from main.classes import Aliment, Ingredient, Recipe


@pytest.fixture
def sample_aliment() -> Aliment:
    al = Aliment(name='onion', tags=['vegetable', 'favorite'])
    yield al


@pytest.fixture
def sample_ingredient(sample_aliment) -> Ingredient:
    ing = Ingredient(aliment=sample_aliment, quantity=10.0, quantity_type='gr')
    yield ing


@pytest.fixture
def sample_recipe(sample_ingredient) -> Recipe:
    recipe = Recipe(name='Fried onions', num_people=2, ingredients=[sample_ingredient],
                    steps=['Chop the onion', 'Fry it!'], category='Main', tags=['Quick', 'vegan'], time=20)
    yield recipe


@pytest.fixture(scope='session')
def sqlite_con():
    sqlite_con = get_unique_instance(database_path='database/despensa_test.sqlite')
    yield sqlite_con


@pytest.fixture()
def sqlite_con_create_database(sqlite_con: SQLiteConnector):
    with open('../main/database/create_tables.sql', 'r') as create_tables_sql_file:
        create_tables_sql_commands = create_tables_sql_file.read().split(';')
        for command in create_tables_sql_commands:
            sqlite_con.execute(command)


class TestSQLiteConnectorAliment:
    @pytest.mark.usefixtures("sqlite_con_create_database")
    def test_aliment_to_sqlite(self, sqlite_con: SQLiteConnector, sample_aliment: Aliment):
        sqlite_con.add_aliment(aliment=sample_aliment)
        aliment_rae = sqlite_con.query("SELECT * FROM aliment WHERE name = 'onion'")[0]
        assert aliment_rae[AlimentTable.NAME] == sample_aliment.name and \
               aliment_rae[AlimentTable.TAGS] == ' '.join(sample_aliment.tags)

    @pytest.mark.usefixtures("sqlite_con_create_database")
    def test_aliment_to_sqlite_id(self, sqlite_con: SQLiteConnector, sample_aliment: Aliment):
        sqlite_con.add_aliment(aliment=sample_aliment)
        aliment_raw = sqlite_con.query("SELECT * FROM aliment WHERE name = 'onion'")[0]

        assert aliment_raw[AlimentTable.ID] != 0

    @pytest.mark.usefixtures("sqlite_con_create_database")
    def test_sqlite_to_aliment(self, sqlite_con: SQLiteConnector, sample_aliment: Aliment):
        sqlite_con.add_aliment(aliment=sample_aliment)

        aliment_raw = sqlite_con.query("SELECT * FROM aliment WHERE name = 'onion'")[0]
        al2 = sqlite_con.db_to_aliment(aliment_raw)

        assert sample_aliment == al2
