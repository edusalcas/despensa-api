import sqlite3
import controller

from classes import Aliment, Ingredient, Recipe
from singleton import Singleton


def clean_connection(func):
    def inner(self, *args, **kwargs):
        con = sqlite3.connect(self.db_path)
        res = func(self, con, *args, **kwargs)
        con.close()

        return res

    return inner


class SQLiteConnector(metaclass=Singleton):

    def __init__(self, database_path):
        self.db_path = database_path

    @clean_connection
    def add_aliment(self, con: sqlite3.Connection, aliment: Aliment):
        name = aliment.name
        tags = ' '.join(aliment.tags)

        cur = con.cursor()
        sql = f"INSERT INTO aliment (name, tags) VALUES ('{name}', '{tags}');"
        cur.execute(sql)

        aliment.set_bd_id(cur.lastrowid)
        con.commit()

    @clean_connection
    def add_ingredient(self, con: sqlite3.Connection, ingredient: Ingredient):
        aliment_id = ingredient.aliment.bd_id
        quantity = ingredient.quantity
        quantity_type = ingredient.quantity_type
        optional = ingredient.optional

        cur = con.cursor()
        sql = f"""
            INSERT INTO ingredient (aliment_id, quantity, quantity_type, optional) 
                VALUES ({aliment_id}, {quantity}, '{quantity_type}', {optional});
        """
        cur.execute(sql)

        ingredient.set_bd_id(cur.lastrowid)
        con.commit()

    def add_recipe_and_ingredients(self, recipe: Recipe):
        for ingredient in recipe.ingredients:
            self.add_ingredient(ingredient)

        self.add_recipe(recipe)
        self.add_recipe_ingredients(recipe)

    @clean_connection
    def add_recipe(self, con: sqlite3.Connection, recipe: Recipe):
        name = recipe.name
        num_people = recipe.num_people
        steps = '\n'.join(recipe.steps)
        category = recipe.category
        tags = ' '.join(recipe.tags)
        time = recipe.time

        cur = con.cursor()
        sql = f"""
            INSERT INTO recipe (name, num_people, steps, category, tags, time)
                VALUES ('{name}', {num_people}, '{steps}', '{category}', '{tags}', {time});
        """
        cur.execute(sql)

        recipe.set_bd_id(cur.lastrowid)
        con.commit()

    @clean_connection
    def add_recipe_ingredients(self, con: sqlite3.Connection, recipe: Recipe):
        recipe_id = recipe.bd_id
        data = [(recipe_id, ingredient.bd_id) for ingredient in recipe.ingredients]

        cur = con.cursor()

        sql = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?) "
        cur.executemany(sql, data)

        con.commit()

    @staticmethod
    def db_to_aliment(aliment_raw: list) -> Aliment:
        bd_id = aliment_raw[0]
        name = aliment_raw[1]
        tags = aliment_raw[2].split(' ')

        return Aliment(name, tags, bd_id)

    @staticmethod
    def db_to_aliment(aliment_raw: list) -> Aliment:
        bd_id = aliment_raw[0]
        name = aliment_raw[1]
        tags = aliment_raw[2].split(' ')

        return Aliment(name, tags, bd_id)

    @staticmethod
    def db_to_ingredient(ingredient_raw: list) -> Ingredient:
        bd_id = int(ingredient_raw[0])
        aliment_id = int(ingredient_raw[1])
        aliment = controller.get_unique_instance().get_aliment_by_id(aliment_id)
        quantity = float(ingredient_raw[2])
        quantity_type = ingredient_raw[3]
        optional = ingredient_raw[4]

        return Ingredient(aliment, quantity, quantity_type, optional, bd_id)

    def db_to_recipe(self, recipe_raw: list) -> Recipe:
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

    # region Get Catalogs
    @clean_connection
    def get_all_aliments(self, con: sqlite3.Connection):
        cur = con.cursor()
        sql = "SELECT * FROM aliment"
        res = cur.execute(sql)
        aliments_raw = res.fetchall()

        aliments = list(map(self.db_to_aliment, aliments_raw))
        return aliments

    @clean_connection
    def get_all_recipes(self, con: sqlite3.Connection):
        cur = con.cursor()

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


unique_instance = None


def get_unique_instance() -> SQLiteConnector:
    global unique_instance

    if unique_instance is None:
        unique_instance = SQLiteConnector('database/despensa.sqlite')
    return unique_instance
