from despensa.catalogs.aliment_catalog import AlimentCatalog
from despensa.catalogs.pantry import Pantry
from despensa.classes import Aliment, Ingredient, Recipe
from despensa.singleton_meta import SingletonMeta

from despensa.sqlite_connector import SQLiteConnector

from typing import List


class Controller(metaclass=SingletonMeta):
    def __init__(self):
        self.db_connector: SQLiteConnector = SQLiteConnector()

        self.__aliments_catalog = AlimentCatalog(self.db_connector)
        self.__recipes_catalog = self.db_connector.get_all_recipes()
        self.__pantry = Pantry(self.db_connector)
        self.__shopping_list = self.db_connector.get_shopping_list()

    def create_aliment(self, name: str, tags: List[str]) -> bool:
        return self.__aliments_catalog.create_aliment(name, tags)

    def insert_aliment_in_pantry(self, name: str) -> bool:
        aliment = self.__aliments_catalog.get_aliment_by_name(name)
        if not aliment:
            return False
        return self.__pantry.add_aliment_to_pantry(aliment)

    def remove_aliment_in_pantry(self, name: str) -> None:
        self.__pantry.remove_aliment_from_pantry(name)

    def update_aliment(self, name: str, tags: List[str]):
        self.__aliments_catalog.update_aliment(name, tags)

    def create_ingredient(self, aliments_name: str, quantity: float, quantity_type: str,
                          optional: bool) -> Ingredient or None:
        aliment = self.get_aliment_by_name(aliments_name)
        if aliment is None:
            return None

        ingredient = Ingredient(aliment, quantity, quantity_type, optional)
        return ingredient

    @staticmethod
    def create_recipe(recipe_name: str, num_people: int, ingredients: List[Ingredient], steps: List[str],
                      category: str, tags: List[str], time: int) -> Recipe:
        recipe = Recipe(recipe_name, num_people, ingredients, steps, category, tags, time)

        return recipe

    def insert_recipe(self, recipe: Recipe):
        self.db_connector.add_recipe_and_ingredients(recipe)
        self.__recipes_catalog.append(recipe)

    def get_recipes_from_pantry(self) -> List[Recipe]:
        aliments_in_pantry = self.get_pantry()
        return [recipe for recipe in self.__recipes_catalog
                if set(recipe.get_not_optional_aliments()) <= set(aliments_in_pantry)]

    def insert_item_in_shopping_list(self, item: str):
        self.db_connector.insert_item_in_shopping_list(item)
        self.__shopping_list.append(item)

    #####################################
    #              Getters              #
    #####################################

    def get_aliment_by_name(self, aliment_name: str) -> Aliment or None:
        return self.__aliments_catalog.get_aliment_by_name(aliment_name)

    def get_aliment_by_id(self, aliment_id: int) -> Aliment or None:
        return self.__aliments_catalog.get_aliment_by_id(aliment_id)

    def get_all_aliments(self) -> List[Aliment]:
        return self.__aliments_catalog.get_all()

    def get_recipes_catalog(self) -> List[Recipe]:
        return self.__recipes_catalog.copy()

    def get_pantry(self) -> List[Aliment]:
        return self.__pantry.get_all()

    def get_shopping_list(self) -> List[str]:
        return self.__shopping_list.copy()
