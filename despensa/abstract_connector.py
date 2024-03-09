from abc import ABC, abstractmethod
from typing import Callable, List

from despensa.classes import Aliment, Ingredient, Recipe
from despensa.singleton_meta import Singleton


class AbstractConnector(ABC, Singleton):
    # region CRUD Aliment
    @abstractmethod
    def add_aliment(self, aliment: Aliment):
        pass

    @abstractmethod
    def get_aliment_by_id(self, aliment_id: int) -> Aliment:
        pass

    @abstractmethod
    def remove_aliment(self, aliment: Aliment):
        pass

    @abstractmethod
    def update_aliment(self, aliment: Aliment):
        pass

    # endregion

    # region CRUD Ingredient
    @abstractmethod
    def add_ingredient(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        pass

    @abstractmethod
    def remove_ingredient(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def update_ingredient(self, ingredient: Ingredient):
        pass

    # endregion

    # region CRUD Recipe

    @abstractmethod
    def add_recipe(self, recipe: Recipe):
        pass

    @abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        pass

    @abstractmethod
    def remove_recipe(self, recipe: Recipe):
        pass

    @abstractmethod
    def update_recipe(self, recipe: Recipe):
        pass

    # endregion

    # region Catalgos
    @abstractmethod
    def get_all_aliments(self) -> List[Aliment]:
        pass

    @abstractmethod
    def get_all_recipes(self) -> List[Recipe]:
        pass

    @abstractmethod
    def get_shopping_list(self) -> List[str]:
        pass

    @abstractmethod
    def get_pantry(self) -> List[Aliment]:
        pass

    # endregion

    # region Shopping list
    @abstractmethod
    def insert_item_in_shopping_list(self, item: str):
        pass

    @abstractmethod
    def remove_item_in_shopping_list(self, item: str):
        pass

    # endregion

    # region Pantry
    @abstractmethod
    def add_aliment_to_pantry(self, aliment: Aliment):
        pass

    @abstractmethod
    def remove_aliment_from_pantry(self, aliment: Aliment):
        pass
    # endregion

    @abstractmethod
    def execute(self, sql: str):
        pass

    @abstractmethod
    def query(self, sql: str) -> List[str]:
        pass
