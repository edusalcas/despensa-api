import pytest
import os

from despensa.classes import Aliment, Ingredient, Recipe
from despensa.sqlite_connector import SQLiteConnector
from environment import Environment
from definitions import MAIN_DIR

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
def sqlite_con():
    sqlite_con = SQLiteConnector()

    yield sqlite_con
    if os.path.exists(sqlite_con.db_path):
        os.remove(sqlite_con.db_path)


class TestSQLiteConnectorAliment:
    def test_aliment_to_sqlite(self, sqlite_con: SQLiteConnector, sample_aliment: Aliment):
        sqlite_con.add_aliment(aliment=sample_aliment)
        db_aliment = sqlite_con.get_aliment_by_id(sample_aliment.db_id)
        assert sample_aliment == db_aliment

    def test_get_aliment_catalog(self, sqlite_con: SQLiteConnector):
        al0 = Aliment(name='onion', tags=['vegetable', 'favorite'])
        al1 = Aliment(name='chicken', tags=['meat'])
        al2 = Aliment(name='olive oil', tags=['oil'])

        sqlite_con.add_aliment(al0)
        sqlite_con.add_aliment(al1)
        sqlite_con.add_aliment(al2)

        db_aliments = sqlite_con.get_all_aliments()

        assert [al0, al1, al2] == db_aliments

    def test_add_aliment_to_pantry(self, sqlite_con: SQLiteConnector):
        al0 = Aliment(name='onion', tags=['vegetable', 'favorite'])
        al1 = Aliment(name='chicken', tags=['meat'])

        sqlite_con.add_aliment(al0)
        sqlite_con.add_aliment(al1)

        sqlite_con.add_ingredient_to_pantry(al0)
        sqlite_con.add_ingredient_to_pantry(al1)

        pantry = sqlite_con.get_pantry()

        assert [al0, al1] == pantry

    def test_remove_aliment_from_pantry(self, sqlite_con: SQLiteConnector):
        al0 = Aliment(name='onion', tags=['vegetable', 'favorite'])
        al1 = Aliment(name='chicken', tags=['meat'])

        sqlite_con.add_aliment(al0)
        sqlite_con.add_aliment(al1)

        sqlite_con.add_ingredient_to_pantry(al0)
        sqlite_con.add_ingredient_to_pantry(al1)

        sqlite_con.remove_ingredient_from_pantry(al0)
        pantry = sqlite_con.get_pantry()

        assert [al1] == pantry


class TestSQLiteConnectionIngredient:
    def test_ingredient_to_sqlite(self, sqlite_con: SQLiteConnector, sample_ingredient: Ingredient):
        sqlite_con.add_aliment(aliment=sample_ingredient.aliment)
        sqlite_con.add_ingredient(ingredient=sample_ingredient)
        db_aliment = sqlite_con.get_ingredient_by_id(sample_ingredient.db_id)
        assert sample_ingredient == db_aliment


class TestSQLiteConnectorRecipe:
    def test_recipe_to_sqlite(self, sqlite_con: SQLiteConnector, sample_recipe):
        for ingredient in sample_recipe.ingredients:
            sqlite_con.add_aliment(ingredient.aliment)
        sqlite_con.add_recipe_and_ingredients(sample_recipe)
        db_recipe = sqlite_con.get_recipe_by_id(sample_recipe.db_id)

        assert sample_recipe == db_recipe

    def test_get_recipes_catalog(self, sqlite_con: SQLiteConnector):
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

        sqlite_con.add_aliment(al0)
        sqlite_con.add_aliment(al1)
        sqlite_con.add_aliment(al2)
        sqlite_con.add_recipe_and_ingredients(re0)
        sqlite_con.add_recipe_and_ingredients(re1)

        db_recipes = sqlite_con.get_all_recipes()

        assert db_recipes == [re0, re1]


class TestSQLiteConnectorShoppingList:
    def test_add_item_to_shopping_list(self, sqlite_con: SQLiteConnector):
        sqlite_con.insert_item_in_shopping_list("Oranges")
        sqlite_con.insert_item_in_shopping_list("Onion")

        assert sqlite_con.get_shopping_list() == ['Oranges', 'Onion']
