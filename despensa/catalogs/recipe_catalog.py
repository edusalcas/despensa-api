from typing import Union, List

from despensa.classes import Recipe
from despensa.singleton_meta import WeakSingletonMeta
from despensa.sqlite_connector import SQLiteConnector
from despensa.catalogs.pantry import Pantry


class RecipeCatalog(metaclass=WeakSingletonMeta):
    def __init__(self, db_connector: SQLiteConnector):
        self.__db_connector: SQLiteConnector = db_connector
        self.__recipe_list: list[Recipe] = db_connector.get_all_recipes()
        self.__recipe_id_map: dict[int, Recipe] = dict(zip([a.db_id for a in self.__recipe_list], self.__recipe_list))

    def get_all(self) -> list[Recipe]:
        return self.__recipe_list.copy()

    def add_recipe(self, recipe: Recipe) -> bool:
        if recipe in self.__recipe_list:
            return False

        self.__db_connector.add_recipe_and_ingredients(recipe)
        self.__recipe_list.append(recipe)
        self.__recipe_id_map[recipe.db_id] = recipe

        return True

    def get_recipes_from_pantry(self) -> List[Recipe]:
        aliments_in_pantry = Pantry(self.__db_connector).get_all()
        available_recipes = [recipe for recipe in self.__recipe_list if set(recipe.get_not_optional_aliments()) <= set(aliments_in_pantry)]
        return available_recipes

    def get_recipe_by_id(self, recipe_id: int) -> Union[Recipe, None]:
        return self.__recipe_id_map.get(recipe_id, None)