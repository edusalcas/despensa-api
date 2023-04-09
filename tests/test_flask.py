import pytest
import json

from despensa.classes import Aliment, Recipe, Ingredient
from despensa.controller import Controller
from despensa.sqlite_connector import SQLiteConnector
from despensa_flask import create_app
from environment import Environment


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    Environment().working_is_test()
    # TODO: Add sample data to database
    SQLiteConnector().generate_sample_data()

    yield app

    # TODO: Clean database


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class TestAliment:
    base_url: str = "/rest/aliments"

    def test_get_all_aliments(self, client):
        response = client.get(self.base_url)
        aliments = Controller().get_all_aliments()
        aliments_flask = [Aliment.from_json(aliment_json) for aliment_json in response.json]

        assert aliments == aliments_flask

    def test_get_aliment(self, client):
        db_id: int = 1
        response = client.get(f"{self.base_url}/{db_id}")
        aliment = Controller().get_aliment_by_id(db_id)
        aliment_flask = Aliment.from_json(response.json)

        assert aliment == aliment_flask

    def test_update_aliment(self, client):
        db_id: int = 1
        client.put(f"{self.base_url}/{db_id}", json={'bd_id': 1, 'name': 'Onion', 'tags': ['vegetable', 'bad']})

        response = client.get(f"{self.base_url}/{db_id}")
        aliment = Controller().get_aliment_by_id(db_id)
        aliment_flask = Aliment.from_json(response.json)

        assert aliment == aliment_flask

    def test_create_aliment(self, client):
        aliment: Aliment = Aliment(name='Oil', tags=['good', 'healthy'])
        aliments = Controller().get_all_aliments()
        client.post(self.base_url, json={'name': 'Oil', 'tags': ['good', 'healthy'], 'db_id': 0})
        aliments_new = Controller().get_all_aliments()

        assert aliments + [aliment] == aliments_new

    def test_delete_aliment(self, client):
        db_id: int = 1
        aliments = [al for al in Controller().get_all_aliments() if al.db_id != db_id]
        client.delete(f"{self.base_url}/{db_id}")
        aliments_new = Controller().get_all_aliments()

        assert aliments == aliments_new


class TestRecipe:
    base_url: str = "/rest/recipes"

    def test_get_all_recipes(self, client):
        response = client.get(self.base_url)
        recipes = Controller().get_recipes_catalog()
        recipes_flask = [Recipe.from_json(recipe_json) for recipe_json in response.json]

        assert recipes == recipes_flask

    def test_get_recipe(self, client):
        db_id: int = 1
        response = client.get(f"{self.base_url}/{db_id}")
        recipe = Controller().get_recipe_by_id(db_id)
        recipe_flask = Recipe.from_json(response.json)

        assert recipe == recipe_flask

    def test_update_recipe(self, client):
        db_id: int = 1
        new_ingredients = [
            Ingredient(aliment=Controller().get_aliment_by_id(1), quantity=1, quantity_type='unit'),
            Ingredient(aliment=Controller().get_aliment_by_id(2), quantity=2, quantity_type='g')
        ]
        recipe = Recipe(name='Fried onions', num_people=2, ingredients=new_ingredients, steps=['Chop the onion', 'Fry it!'], category='Main')
        client.put(f"{self.base_url}/{db_id}", json=recipe.__dict__)

        response = client.get(f"{self.base_url}/{db_id}")
        recipe_updated = Recipe.from_json(response.json)

        assert recipe == recipe_updated

    def test_create_recipe(self, client):
        new_ingredients = [
            Ingredient(aliment=Controller().get_aliment_by_id(1), quantity=1, quantity_type='unit'),
            Ingredient(aliment=Controller().get_aliment_by_id(2), quantity=2, quantity_type='g')
        ]
        recipe = Recipe(name='Fried onions 2', num_people=4, ingredients=new_ingredients, steps=['Chop the onion', 'Fry it!'], category='Main')
        recipes = Controller().get_recipes_catalog()
        client.post(self.base_url, json=recipe.__dict__)
        recipes_new = Controller().get_recipes_catalog()

        assert recipes + [recipe] == recipes_new

    def test_delete_recipe(self, client):
        db_id: int = 1
        recipes = [r for r in Controller().get_recipes_catalog() if r.db_id != db_id]
        client.delete(f"{self.base_url}/{db_id}")
        recipes_new = Controller().get_recipes_catalog()

        assert recipes == recipes_new


class TestPantry:
    base_url: str = "/rest/pantry"

    def test_get_pantry(self, client):
        response = client.get(self.base_url)
        pantry = Controller().get_pantry()
        pantry_flask = [Aliment.from_json(recipe_json) for recipe_json in response.json]

        assert pantry == pantry_flask

    def test_add_aliment_to_pantry(self, client):
        new_aliment = Controller().get_aliment_by_id(3)
        pantry = Controller().get_pantry()
        client.post(f"{self.base_url}/{new_aliment.name}")
        pantry_new = Controller().get_pantry()

        assert pantry + [new_aliment] == pantry_new

    def test_delete_recipe(self, client):
        old_aliment = Controller().get_aliment_by_id(1)
        pantry = [p for p in Controller().get_pantry() if p.name != old_aliment.name]
        client.delete(f"{self.base_url}/{old_aliment.name}")
        pantry_new = Controller().get_pantry()

        assert pantry == pantry_new


class TestShoppingList:
    base_url: str = "/rest/shopping_list"

    def test_get_shopping_list(self, client):
        response = client.get(self.base_url)
        shopping_list = Controller().get_shopping_list()
        shopping_list_flask = response.json

        assert shopping_list == shopping_list_flask

    def test_add_aliment_to_shopping_list(self, client):
        new_item = 'item_new'
        shopping_list = Controller().get_shopping_list()
        client.post(f"{self.base_url}/{new_item}")
        shopping_list_new = Controller().get_shopping_list()

        assert shopping_list + [new_item] == shopping_list_new

    def test_delete_recipe(self, client):
        old_item = 'item1'
        shopping_list = [p for p in Controller().get_shopping_list() if p != old_item]
        client.delete(f"{self.base_url}/{old_item}")
        shopping_list_new = Controller().get_shopping_list()

        assert shopping_list == shopping_list_new
