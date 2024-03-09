import pytest

from despensa.classes import Aliment, Ingredient, Recipe
from despensa.abstract_connector import AbstractConnector
from despensa.database_connector_factory import DatabaseConnectorFactory
from environment import Environment
import definitions as d

Environment().working_is_test()


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


@pytest.fixture
def connector():
    Environment().set_current_database(d.POSTGRES)
    connector: AbstractConnector = DatabaseConnectorFactory.get_database_connector()
    connector.clear_all_tables()
    connector.create_all_tables()
    yield connector


class TestConnectorAliment:
    def test_aliment_to_sqlite(self, connector: AbstractConnector, sample_aliment: Aliment):
        connector.add_aliment(aliment=sample_aliment)
        db_aliment = connector.get_aliment_by_id(sample_aliment.db_id)
        assert sample_aliment == db_aliment

    def test_get_aliment_catalog(self, connector: AbstractConnector):
        al0 = Aliment(name='onion', tags=['vegetable', 'favorite'])
        al1 = Aliment(name='chicken', tags=['meat'])
        al2 = Aliment(name='olive oil', tags=['oil'])

        connector.add_aliment(al0)
        connector.add_aliment(al1)
        connector.add_aliment(al2)

        db_aliments = connector.get_all_aliments()

        assert [al0, al1, al2] == db_aliments

    @staticmethod
    def add_aliments_to_pantry(connector):
        al0 = Aliment(name='onion', tags=['vegetable', 'favorite'])
        al1 = Aliment(name='chicken', tags=['meat'])
        connector.add_aliment(al0)
        connector.add_aliment(al1)
        connector.add_aliment_to_pantry(al0)
        connector.add_aliment_to_pantry(al1)
        return al0, al1

    def test_add_aliment_to_pantry(self, connector: AbstractConnector):
        al0, al1 = self.add_aliments_to_pantry(connector)

        pantry = connector.get_pantry()

        assert [al0, al1] == pantry

    def test_remove_aliment_from_pantry(self, connector: AbstractConnector):
        al0, al1 = self.add_aliments_to_pantry(connector)

        connector.remove_aliment_from_pantry(al0)
        pantry = connector.get_pantry()

        assert [al1] == pantry


class TestSQLiteConnectionIngredient:
    def test_ingredient_to_sqlite(self, connector: AbstractConnector, sample_ingredient: Ingredient):
        connector.add_aliment(aliment=sample_ingredient.aliment)
        connector.add_ingredient(ingredient=sample_ingredient)
        db_aliment = connector.get_ingredient_by_id(sample_ingredient.db_id)
        assert sample_ingredient == db_aliment


class TestAbstractConnectorRecipe:
    def test_recipe_to_sqlite(self, connector: AbstractConnector, sample_recipe):
        for ingredient in sample_recipe.ingredients:
            connector.add_aliment(ingredient.aliment)
        connector.add_recipe(sample_recipe)
        db_recipe = connector.get_recipe_by_id(sample_recipe.db_id)

        assert sample_recipe == db_recipe

    def test_get_recipes_catalog(self, connector: AbstractConnector):
        al0 = Aliment(name='onion', tags=['vegetable', 'favorite'])
        al1 = Aliment(name='chicken', tags=['meat'])
        al2 = Aliment(name='olive oil', tags=['oil'])

        re0 = Recipe(
            name='recipe0',
            num_people=2,
            ingredients=[Ingredient(al0, 10, 'gr'), Ingredient(al2, 1, 'spoon')],
            steps=['Step 1', 'Step 2'],
            tags=['tag1', 'tag2'],
            category='despensa',
            time=10
        )
        re1 = Recipe(
            name='recipe1',
            num_people=4,
            ingredients=[Ingredient(al1, 200, 'gr'), Ingredient(al2, 2, 'spoon')],
            steps=['Step 1', 'Step 2', 'Step 3'],
            tags=['tag3', 'tag2'],
            category='dessert',
            time=30
        )

        connector.add_aliment(al0)
        connector.add_aliment(al1)
        connector.add_aliment(al2)
        connector.add_recipe(re0)
        connector.add_recipe(re1)

        db_recipes = connector.get_all_recipes()

        assert db_recipes == [re0, re1]


class TestAbstractConnectorShoppingList:
    def test_add_item_to_shopping_list(self, connector: AbstractConnector):
        connector.insert_item_in_shopping_list("Oranges")
        connector.insert_item_in_shopping_list("Onion")

        assert connector.get_shopping_list() == ['Oranges', 'Onion']
