from abc import ABC, abstractmethod
from typing import Callable, List

from despensa.classes import Aliment, Ingredient, Recipe
from despensa.singleton_meta import WeakSingletonMeta


class AbstractConnector(ABC):

    def __init__(self):
        __metaclass__ = WeakSingletonMeta

    @abstractmethod
    def clean_connection(func: Callable) -> Callable:
        pass

    # region CRUD Aliment
    @abstractmethod
    def _add_aliment(self, aliment: Aliment):
        pass

    @abstractmethod
    def _get_aliment_by_id(self, aliment_id: int) -> Aliment:
        pass

    @abstractmethod
    def _remove_aliment(self, aliment: Aliment):
        pass

    @abstractmethod
    def _update_aliment(self, aliment: Aliment):
        pass

    # endregion

    # region CRUD Ingredient
    @abstractmethod
    def _add_ingredient(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def _get_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        pass

    @abstractmethod
    def _remove_ingredient(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def _update_ingredient(self, ingredient: Ingredient):
        pass

    # endregion

    # region CRUD Recipe

    @abstractmethod
    def _add_recipe(self, recipe: Recipe):
        pass

    @abstractmethod
    def _get_recipe_by_id(self, recipe_id: int) -> Recipe:
        pass

    @abstractmethod
    def _remove_recipe(self, recipe: Recipe):
        pass

    @abstractmethod
    def _update_recipe(self, recipe: Recipe):
        pass

    # endregion

    # region Catalgos
    @abstractmethod
    def _get_all_aliments(self) -> List[Aliment]:
        pass

    @abstractmethod
    def _get_all_recipes(self) -> List[Recipe]:
        pass

    @abstractmethod
    def _get_shopping_list(self) -> List[str]:
        pass

    @abstractmethod
    def _get_pantry(self) -> List[Aliment]:
        pass

    # endregion

    # region Shopping list
    @abstractmethod
    def _insert_item_in_shopping_list(self, item: str):
        pass

    @abstractmethod
    def _remove_item_in_shopping_list(self, item: str):
        pass

    # endregion

    # region Pantry
    @abstractmethod
    def _add_ingredient_to_pantry(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def _remove_ingredient_from_pantry(self, ingredient: Ingredient):
        pass
    # endregion

    @abstractmethod
    def _execute(self, sql: str):
        pass

    @abstractmethod
    def _query(self, sql: str) -> List[str]:
        pass

    # region Clean Connection methods
    # region Aliment
    @clean_connection
    def add_aliment(self, aliment: Aliment):
        self._add_aliment(aliment)

    @clean_connection
    def get_aliment_by_id(self, aliment_id: int) -> Aliment:
        return self._get_aliment_by_id(aliment_id)

    @clean_connection
    def remove_aliment(self, aliment: Aliment):
        self._remove_aliment(aliment)

    @clean_connection
    def update_aliment(self, aliment: Aliment):
        self._update_aliment(aliment)
    # endregion
    # region Ingredient
    @clean_connection
    def add_ingredient(self, ingredient: Ingredient):
        self._add_ingredient(ingredient)

    @clean_connection
    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        return self._get_ingredient_by_id(ingredient_id)

    @clean_connection
    def remove_ingredient(self, ingredient: Ingredient):
        self._remove_ingredient(ingredient)

    @clean_connection
    def update_ingredient(self, ingredient: Ingredient):
        self._update_ingredient(ingredient)
    # endregion
    # region Recipe
    @clean_connection
    def add_recipe(self, recipe: Recipe):
        self._add_recipe(recipe)

    @clean_connection
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self._get_recipe_by_id(recipe_id)

    @clean_connection
    def remove_recipe(self, recipe: Recipe):
        self._remove_recipe(recipe)

    @clean_connection
    def update_recipe(self, recipe: Recipe):
        self._update_recipe(recipe)
    # endregion
    # region Catalogs
    @clean_connection
    def get_all_aliments(self) -> List[Aliment]:
        return self._get_all_aliments()

    @clean_connection
    def get_all_recipes(self) -> List[Recipe]:
        return self._get_all_recipes()

    @clean_connection
    def get_shopping_list(self) -> List[str]:
        return self._get_shopping_list()

    @clean_connection
    def get_pantry(self) -> List[Aliment]:
        return self._get_pantry()
    # endregion
    # region Shopping List
    @clean_connection
    def insert_item_in_shopping_list(self, item: str):
        self._insert_item_in_shopping_list(item)

    @clean_connection
    def remove_item_in_shopping_list(self, item: str):
        self._remove_item_in_shopping_list(item)
    # endregion
    # region Pantry
    @clean_connection
    def add_ingredient_to_pantry(self, ingredient: Ingredient):
        self._add_ingredient_to_pantry(ingredient)

    @clean_connection
    def remove_ingredient_from_pantry(self, ingredient: Ingredient):
        self._remove_ingredient_from_pantry(ingredient)
    # endregion
    @clean_connection
    def execute(self, sql: str):
        self._execute(sql)

    @clean_connection
    def query(self, sql: str):
        return self._query(sql)
    # endregion
