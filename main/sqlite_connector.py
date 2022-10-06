from main import controller
from main.classes import Aliment, Ingredient, Recipe
from main.singleton import Singleton

import sqlite3

from typing import Callable, List


class AlimentTable():
    ID: int = 0
    NAME: int = 1
    TAGS: int = 2


def clean_connection(func: Callable) -> Callable:
    """This function will serve as a decorator for the class methods in SQLiteConnector. It opens a connection with
    the database and then close it when the job is done

    :param func: The function to decorate
    :return: The function decorated
    """

    def inner(sqlite_ref, *args, **kwargs):
        """ Inner method that ensures to open and close the connection with the database while the job in the
        function is done

        :param sqlite_ref: Reference to a SQLiteConnector object
        :param args: list of arguments
        :param kwargs: dict of arguments
        :return: Returns the value the outer function returns
        """
        sqlite_ref.con = sqlite3.connect(sqlite_ref.db_path)
        res = func(sqlite_ref, *args, **kwargs)
        sqlite_ref.con.close()

        return res

    return inner


class SQLiteConnector(metaclass=Singleton):
    """Clase que implementa la funcionalidad para establecer conexión con una base de datos SQLite y realizar
    operaciones sobre la misma"""

    def __init__(self, database_path):
        self.con = None
        self.db_path: str = database_path

    # region Add functions
    @clean_connection
    def add_aliment(self, aliment: Aliment):
        """Add an aliment to the database

        :param aliment: Aliment to insert in the database
        """
        name = aliment.name
        tags = ' '.join(aliment.tags)

        cur = self.con.cursor()
        sql = f"INSERT INTO aliment (name, tags) VALUES ('{name}', '{tags}');"
        cur.execute(sql)

        aliment.set_bd_id(cur.lastrowid)
        self.con.commit()

    def __add_ingredient(self, ingredient: Ingredient):
        """Insert an ingredient in the database

        :param ingredient: Ingredient to insert
        """
        aliment_id = ingredient.aliment.bd_id
        quantity = ingredient.quantity
        quantity_type = ingredient.quantity_type
        optional = ingredient.optional

        cur = self.con.cursor()
        sql = f"""
            INSERT INTO ingredient (aliment_id, quantity, quantity_type, optional) 
                VALUES ({aliment_id}, {quantity}, '{quantity_type}', {optional});
        """
        cur.execute(sql)

        ingredient.set_bd_id(cur.lastrowid)
        self.con.commit()

    def __add_recipe(self, recipe: Recipe):
        """Insert a recipe in the database

        :param recipe: The recipe to insert
        """
        name = recipe.name
        num_people = recipe.num_people
        steps = '\n'.join(recipe.steps)
        category = recipe.category
        tags = ' '.join(recipe.tags)
        time = recipe.time

        cur = self.con.cursor()
        sql = f"""
            INSERT INTO recipe (name, num_people, steps, category, tags, time)
                VALUES ('{name}', {num_people}, '{steps}', '{category}', '{tags}', {time});
        """
        cur.execute(sql)

        recipe.set_bd_id(cur.lastrowid)
        self.con.commit()

    def __add_recipe_ingredients(self, recipe: Recipe):
        """Insert the ingredients of a recipe in the database

        :param recipe: The recipe with the ingredients to insert
        """
        recipe_id = recipe.bd_id
        data = [(recipe_id, ingredient.bd_id) for ingredient in recipe.ingredients]

        cur = self.con.cursor()

        sql = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?) "
        cur.executemany(sql, data)

        self.con.commit()

    @clean_connection
    def add_recipe_and_ingredients(self, recipe: Recipe):
        """Insert in the database a recipe and its ingredients

        :param recipe: Recipe to insert with its recipe
        """
        for ingredient in recipe.ingredients:
            self.__add_ingredient(ingredient=ingredient)

        self.__add_recipe(recipe=recipe)
        self.__add_recipe_ingredients(recipe=recipe)

    # endregion

    # region DB to object functions

    @staticmethod
    def db_to_aliment(aliment_raw: list) -> Aliment:
        """Transform an aliment from the database to an aliment object

        :param aliment_raw: List of attributes of the aliment
        :return: The aliment object
        """
        bd_id = aliment_raw[AlimentTable.ID]
        name = aliment_raw[AlimentTable.NAME]
        tags = aliment_raw[AlimentTable.TAGS].split(' ')

        return Aliment(name, tags, bd_id)

    @staticmethod
    def db_to_ingredient(ingredient_raw: list) -> Ingredient:
        """Transform an ingredient from the database to an ingredient object

        :param ingredient_raw: List of attributes of the ingredient
        :return: The ingredient object
        """
        bd_id = int(ingredient_raw[0])
        aliment_id = int(ingredient_raw[1])
        aliment = controller.get_unique_instance().get_aliment_by_id(aliment_id)
        quantity = float(ingredient_raw[2])
        quantity_type = ingredient_raw[3]
        optional = ingredient_raw[4]

        return Ingredient(aliment, quantity, quantity_type, optional, bd_id)

    def db_to_recipe(self, recipe_raw: list) -> Recipe:
        """Transform a recipe from the database to a recipe object

        :param recipe_raw: List of attributes of the recipe
        :return: The recipe object
        """
        bd_id = recipe_raw[0]
        name = recipe_raw[1]
        num_people = recipe_raw[2]
        steps = recipe_raw[3].split('\n')
        category = recipe_raw[4]
        tags = recipe_raw[5].split(' ')
        time = recipe_raw[6]
        ingredients_raw = [ingredient_raw.split(',') for ingredient_raw in recipe_raw[7].split(';')]
        ingredients = list(map(self.db_to_ingredient, ingredients_raw))

        return Recipe(name, num_people, ingredients, steps, category, tags, time, bd_id)

    # endregion

    # region Get Catalogs
    @clean_connection
    def get_all_aliments(self) -> list[Aliment]:
        """Get a list of all aliments in the database

        :return: The list of all aliments
        """
        cur = self.con.cursor()
        sql = "SELECT * FROM aliment"
        res = cur.execute(sql)
        aliments_raw = res.fetchall()

        aliments = list(map(self.db_to_aliment, aliments_raw))
        return aliments

    @clean_connection
    def get_all_recipes(self) -> list[Recipe]:
        """Get a list of all recipes in the database

        :return: The list of all recipes in the database
        """
        cur = self.con.cursor()

        sql = """
            SELECT 
                recipe.*,
                group_concat(ingredient_id || ',' || aliment_id || ',' || quantity || ',' || quantity_type || ',' || optional, ';')
            FROM 
                recipe
                INNER JOIN recipe_ingredient USING(recipe_id)
                INNER JOIN ingredient USING(ingredient_id)
            GROUP BY
                recipe_id,
                name,
                num_people,
                steps,
                category,
                tags,
                time
        """
        res = cur.execute(sql)

        recipes_raw = res.fetchall()

        recipes = list(map(self.db_to_recipe, recipes_raw))

        print(recipes)
        return recipes

    # endregion

    @clean_connection
    def execute(self, sql: str):
        """Execute a sql command

        :param sql: Command to execute
        """
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

    @clean_connection
    def query(self, sql: str) -> List[str]:
        """Query to the database

        :param sql: Query
        :return: The list of results
        """
        cur = self.con.cursor()
        res = cur.execute(sql)
        return res.fetchall()


unique_instance = None


def get_unique_instance(database_path: str = 'database/despensa.sqlite') -> SQLiteConnector:
    """This function ensures there is only one instance of the SQLiteConnector class

    :return: The unique instance of the SQLiteConnector
    """
    global unique_instance

    if unique_instance is None:
        unique_instance = SQLiteConnector(database_path)
    return unique_instance
