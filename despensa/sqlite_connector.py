from despensa.abstract_connector import AbstractConnector
from despensa.classes import Aliment, Ingredient, Recipe
from definitions import SQLITE_DB, MAIN_DIR, SQLITE_SAMPLE_DATA
from environment import Environment, SQLiteConfig

import os
import sqlite3

from typing import Callable, List


class AlimentTable:
    ID: int = 0
    NAME: int = 1
    TAGS: int = 2


class IngredientTable:
    ID: int = 0
    ALIMENT_ID = 1
    QUANTITY = 2
    QUANTITY_TYPE = 3
    OPTIONAL = 4


class RecipeTable:
    ID: int = 0
    NAME: int = 1
    NUM_PEOPLE: int = 2
    STEPS: int = 3
    CATEGORY: int = 4
    TAGS: int = 5
    TIME: int = 6


def clean_connection(func: Callable) -> Callable:
    def inner(sqlite_ref, *args, **kwargs):
        close_connection = False
        if sqlite_ref.con is None:  # Create the connection if it is not already created
            sqlite_ref.con = sqlite3.connect(sqlite_ref.config.db_path)
            close_connection = True

        res = func(sqlite_ref, *args, **kwargs)

        if close_connection:  # If the creation has been created in this function call, close it
            sqlite_ref.con.close()
            sqlite_ref.con = None

        return res

    return inner


# noinspection PyArgumentList
class SQLiteConnector(AbstractConnector):
    def __init__(self):
        super().__init__()
        self.con: sqlite3.Connection = None
        self.config: SQLiteConfig = Environment().get_sqlite_config()

    # region CRUD Aliment
    @clean_connection
    def add_aliment(self, aliment: Aliment):
        name = aliment.name
        tags = ' '.join(aliment.tags)

        cur = self.con.cursor()
        sql = f"INSERT INTO aliment (name, tags) VALUES ('{name}', '{tags}');"
        cur.execute(sql)

        aliment.set_db_id(cur.lastrowid)
        self.con.commit()

    @clean_connection
    def get_aliment_by_id(self, aliment_id: int) -> Aliment:
        cur = self.con.cursor()
        aliment_raw = cur.execute(f"SELECT * FROM aliment WHERE aliment_id = {aliment_id}").fetchone()
        aliment = self.db_to_aliment(aliment_raw)

        return aliment

    @clean_connection
    def remove_aliment(self, aliment: Aliment):
        cur = self.con.cursor()
        cur.execute(f"PRAGMA foreign_keys = ON")
        cur.execute(f"DELETE FROM aliment WHERE aliment_id = {aliment.db_id}")
        self.con.commit()

    @clean_connection
    def update_aliment(self, aliment: Aliment):
        name = aliment.name
        tags = ' '.join(aliment.tags)

        cur = self.con.cursor()
        sql = f"UPDATE aliment SET tags = '{tags}' WHERE name = '{name}';"
        cur.execute(sql)
        self.con.commit()

    # endregion

    # region CRUD Ingredient
    @clean_connection
    def add_ingredient(self, ingredient: Ingredient):
        aliment_id = ingredient.aliment.db_id
        quantity = ingredient.quantity
        quantity_type = ingredient.quantity_type
        optional = ingredient.optional

        cur = self.con.cursor()
        sql = f"""
            INSERT INTO ingredient (aliment_id, quantity, quantity_type, optional) 
                VALUES ({aliment_id}, {quantity}, '{quantity_type}', {optional});
        """
        cur.execute(sql)

        ingredient.set_db_id(cur.lastrowid)
        self.con.commit()

    @clean_connection
    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        cur = self.con.cursor()
        ingredient_raw = cur.execute(f"SELECT * FROM ingredient WHERE ingredient_id = {ingredient_id}").fetchone()
        ingredient = self.db_to_ingredient(ingredient_raw)

        return ingredient

    @clean_connection
    def remove_ingredient(self, ingredient: Ingredient):
        pass

    @clean_connection
    def update_ingredient(self, ingredient: Ingredient):
        pass

    # endregion

    # region CRUD Recipe
    @clean_connection
    def add_recipe(self, recipe: Recipe):
        for ingredient in recipe.ingredients:
            self.add_ingredient(ingredient=ingredient)

        name = recipe.name
        num_people = recipe.num_people
        steps = '\n'.join(recipe.steps)
        category = recipe.category
        tags = ' '.join(recipe.tags)
        time = recipe.time

        cur = self.con.cursor()
        sql = f"""
            INSERT INTO recipe (name, num_people, steps, category, tags, time)
                VALUES ('{name}', {num_people}, '{steps}', '{category}', '{tags}', '{time}');
        """
        cur.execute(sql)

        recipe.set_db_id(cur.lastrowid)

        recipe_id = recipe.db_id
        data = [(recipe_id, ingredient.db_id) for ingredient in recipe.ingredients]

        cur = self.con.cursor()

        sql = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?) "
        cur.executemany(sql, data)

        self.con.commit()

    @clean_connection
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        cur = self.con.cursor()
        recipe_raw = cur.execute(f"SELECT * FROM recipe WHERE recipe_id = {recipe_id}").fetchone()
        ingredients_ids = cur.execute(f"""SELECT ingredient_id FROM recipe_ingredient WHERE recipe_id = {recipe_id}""") \
            .fetchall()
        ingredients_ids = [ingredient_tuple[0] for ingredient_tuple in ingredients_ids]
        recipe = self.db_to_recipe(recipe_raw, ingredients_ids)

        return recipe

    @clean_connection
    def remove_recipe(self, recipe: Recipe):
        cur = self.con.cursor()

        cur.execute(f"PRAGMA foreign_keys = ON")
        sql = f"DELETE FROM recipe WHERE recipe_id = {recipe.db_id}"
        cur.execute(sql)
        self.con.commit()

    @clean_connection
    def update_recipe(self, recipe: Recipe):
        cur = self.con.cursor()
        cur.execute(f"PRAGMA foreign_keys = ON")

        sql = f"DELETE FROM ingredient WHERE ingredient_id IN (SELECT ingredient_id FROM recipe_ingredient WHERE recipe_id = {recipe.db_id})"
        cur.execute(sql)
        for ingredient in recipe.ingredients:
            self.add_ingredient(ingredient)

        cur = self.con.cursor()

        recipe_id = recipe.db_id
        data = [(recipe_id, ingredient.db_id) for ingredient in recipe.ingredients]

        sql = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?) "
        cur.executemany(sql, data)

        self.con.commit()

        name = recipe.name
        num_people = recipe.num_people
        steps = '\n'.join(recipe.steps)
        category = recipe.category
        tags = ' '.join(recipe.tags)
        time = recipe.time
        sql = f"""
            UPDATE recipe 
            SET 
                name='{name}', num_people='{num_people}', steps='{steps}', category='{category}', tags='{tags}', time='{time}' 
            WHERE recipe_id = {recipe.db_id};"""
        cur.execute(sql)
        self.con.commit()

    # endregion

    # region Catalgos
    @clean_connection
    def get_all_aliments(self) -> List[Aliment]:
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM aliment")
        aliments_raw = res.fetchall()

        aliments = list(map(self.db_to_aliment, aliments_raw))
        return aliments

    @clean_connection
    def get_all_recipes(self) -> List[Recipe]:
        cur = self.con.cursor()
        res = cur.execute("SELECT recipe_id FROM recipe")

        recipes_ids = [row[0] for row in res.fetchall()]

        recipes = list(map(self.get_recipe_by_id, recipes_ids))

        return recipes

    @clean_connection
    def get_shopping_list(self) -> List[str]:
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM shopping_list")
        items_raw = res.fetchall()
        items = [i[0] for i in items_raw]

        return items

    @clean_connection
    def get_pantry(self) -> List[Aliment]:
        cur = self.con.cursor()
        res = cur.execute("SELECT aliment.* FROM pantry INNER JOIN aliment USING(aliment_id)")
        aliments_raw = res.fetchall()

        pantry = list(map(self.db_to_aliment, aliments_raw))
        return pantry

    # endregion

    # region Shopping list
    @clean_connection
    def insert_item_in_shopping_list(self, item: str):
        cur = self.con.cursor()
        sql = f"INSERT INTO shopping_list (item) VALUES ('{item}')"
        cur.execute(sql)

        self.con.commit()

    @clean_connection
    def remove_item_in_shopping_list(self, item: str):
        cur = self.con.cursor()
        sql = f"DELETE FROM shopping_list WHERE item = '{item}'"
        cur.execute(sql)

        self.con.commit()

    # endregion

    # region Pantry
    @clean_connection
    def add_aliment_to_pantry(self, ingredient: Ingredient):
        cur = self.con.cursor()
        sql = f"""
            INSERT INTO pantry (aliment_id) 
                VALUES ({ingredient.db_id});
        """
        cur.execute(sql)
        self.con.commit()

    @clean_connection
    def remove_aliment_from_pantry(self, ingredient: Ingredient):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM pantry WHERE aliment_id = {ingredient.db_id};")
        self.con.commit()

    # endregion

    # region DB to object functions

    @staticmethod
    def db_to_aliment(aliment_raw: list) -> Aliment:
        bd_id = aliment_raw[AlimentTable.ID]
        name = aliment_raw[AlimentTable.NAME]
        tags = aliment_raw[AlimentTable.TAGS].split(' ')

        return Aliment(name, tags, bd_id)

    def db_to_ingredient(self, ingredient_raw: list) -> Ingredient:

        bd_id = int(ingredient_raw[IngredientTable.ID])
        aliment = self.get_aliment_by_id(int(ingredient_raw[IngredientTable.ALIMENT_ID]))
        quantity = float(ingredient_raw[IngredientTable.QUANTITY])
        quantity_type = ingredient_raw[IngredientTable.QUANTITY_TYPE]
        optional = ingredient_raw[IngredientTable.OPTIONAL]

        return Ingredient(aliment, quantity, quantity_type, optional, bd_id)

    def db_to_recipe(self, recipe_raw: list, ingredients_ids: list) -> Recipe:

        bd_id = recipe_raw[RecipeTable.ID]
        name = recipe_raw[RecipeTable.NAME]
        num_people = recipe_raw[RecipeTable.NUM_PEOPLE]
        steps = recipe_raw[RecipeTable.STEPS].split('\n')
        category = recipe_raw[RecipeTable.CATEGORY]
        tags = recipe_raw[RecipeTable.TAGS].split(' ') if recipe_raw[RecipeTable.TAGS] != '' else []
        time = recipe_raw[RecipeTable.TIME] if recipe_raw[RecipeTable.TIME] != 'None' else None
        ingredients = list(map(self.get_ingredient_by_id, ingredients_ids))

        return Recipe(name, num_people, ingredients, steps, category, tags, time, bd_id)

    # endregion

    @clean_connection
    def execute(self, sql: str):
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

    @clean_connection
    def query(self, sql: str) -> List[str]:
        cur = self.con.cursor()
        res = cur.execute(sql)
        return res.fetchall()

    @clean_connection
    def generate_sample_data(self):
        if Environment().get_current_env() == 1:
            with open(SQLITE_SAMPLE_DATA, 'r') as sample_data_sql_file:
                sample_data_sql_commands = sample_data_sql_file.read().split(';')
                for command in sample_data_sql_commands:
                    self.execute(command)
