from despensa.abstract_connector import AbstractConnector
from despensa.catalogs.aliment_catalog import AlimentCatalog
from despensa.catalogs.pantry import Pantry
from despensa.catalogs.recipe_catalog import RecipeCatalog
from despensa.catalogs.shopping_list import ShoppingList
from despensa.classes import Aliment, Ingredient, Recipe
from despensa.singleton_meta import WeakSingletonMeta

from despensa.database_connector_factory import DatabaseConnectorFactory

from typing import List, Union


class Controller(metaclass=WeakSingletonMeta):
    def __init__(self):
        self.__db_connector: AbstractConnector = DatabaseConnectorFactory.get_database_connector()

        self.__aliments_catalog = AlimentCatalog(self.__db_connector)
        self.__recipes_catalog = RecipeCatalog(self.__db_connector)
        self.__pantry = Pantry(self.__db_connector)
        self.__shopping_list = ShoppingList(self.__db_connector)

    def create_aliment(self, name: str, tags: List[str]) -> Aliment:
        return self.__aliments_catalog.create_aliment(name, tags)

    def create_aliment_from_json(self, json: dict) -> Aliment:
        return self.__aliments_catalog.create_aliment_from_json(json)

    def insert_aliment_in_pantry(self, name: str) -> List[Aliment]:
        return self.__pantry.add_aliment_to_pantry(name)

    def remove_aliment_in_pantry(self, name: str) -> None:
        self.__pantry.remove_aliment_from_pantry(name)

    def update_aliment(self, name: str, tags: List[str]):
        self.__aliments_catalog.update_aliment(name, tags)

    def update_aliment_from_json(self, id_aliment: int, json: dict):
        self.__aliments_catalog.update_aliment_from_json(id_aliment, json)

    def delete_aliment(self, aliment_id: int):
        self.__aliments_catalog.delete_aliment(aliment_id)

    def create_ingredient(self, aliments_name: str, quantity: float, quantity_type: str,
                          optional: bool) -> Ingredient or None:
        aliment = self.get_aliment_by_name(aliments_name)
        if aliment is None:
            return None

        ingredient = Ingredient(aliment, quantity, quantity_type, optional)
        return ingredient

    @staticmethod
    def create_recipe(recipe_name: str, num_people: int, ingredients: List[Ingredient], steps: List[str], category: str, tags: List[str], time: int) -> Recipe:
        recipe = Recipe(recipe_name, num_people, ingredients, steps, category, tags, time)

        return recipe

    def create_recipe_from_json(self, json) -> Recipe:
        return self.__recipes_catalog.create_recipe_from_json(json)

    def update_recipe_from_json(self, recipe_id: int, json: dict):
        self.__recipes_catalog.update_recipe_from_json(recipe_id, json)

    def delete_recipe(self, recipe_id):
        self.__recipes_catalog.delete_recipe(recipe_id)

    def insert_recipe(self, recipe: Recipe) -> Recipe:
        return self.__recipes_catalog.add_recipe(recipe)

    def get_recipes_from_pantry(self) -> List[Recipe]:
        return self.__recipes_catalog.get_recipes_from_pantry()

    def insert_item_in_shopping_list(self, item: str):
        self.__shopping_list.add_item_to_shopping_list(item)

    def remove_item_from_shopping_list(self, item: str):
        self.__shopping_list.remove_item_from_shopping_list(item)

    #####################################
    #              Getters              #
    #####################################

    def get_aliment_by_name(self, aliment_name: str) -> Union[Aliment, None]:
        return self.__aliments_catalog.get_aliment_by_name(aliment_name)

    def get_aliment_by_id(self, aliment_id: int) -> Union[Aliment, None]:
        return self.__aliments_catalog.get_aliment_by_id(aliment_id)

    def get_recipe_by_id(self, recipe_id: int) -> Union[Recipe, None]:
        return self.__recipes_catalog.get_recipe_by_id(recipe_id)

    def get_all_aliments(self) -> List[Aliment]:
        return self.__aliments_catalog.get_all()

    def get_recipes_catalog(self) -> List[Recipe]:
        return self.__recipes_catalog.get_all()

    def get_pantry(self) -> List[Aliment]:
        return self.__pantry.get_all()

    def get_shopping_list(self) -> List[str]:
        return self.__shopping_list.get_all()
