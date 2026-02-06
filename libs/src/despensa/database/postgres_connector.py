from typing import List

import psycopg2

from despensa.abstract_connector import AbstractConnector
from despensa.objects.classes import Aliment, Ingredient, Recipe
from environment import PostgresConfig, Environment


class PostgresConnector(AbstractConnector):
    def __init__(self):
        super().__init__()
        self.config: PostgresConfig = Environment().get_postgres_config()
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)

    def disconnect(self, exc_type, exc_value, traceback):
        """
        Método que se ejecuta al finalizar el context manager.
        Se encarga de cerrar la conexión y el cursor, y manejar excepciones si las hay.
        """
        try:
            if exc_type is None:
                # Si no hay excepciones, hacer commit
                self.connection.commit()
            else:
                # Si hay alguna excepción, hacer rollback
                print(f"Excepción atrapada: {exc_value}")
                self.connection.rollback()
        finally:
            # Cerrar el cursor y la conexión
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

    # region CRUD Aliment
    def add_aliment(self, aliment: Aliment):
        try:
            sql = (
                "INSERT INTO aliment (name, tags) VALUES (%s, %s) RETURNING aliment_id;"
            )
            self.cursor.execute(sql, (aliment.name, aliment.tags))
            aliment.set_db_id(self.cursor.fetchone()[0])
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error adding aliment:", e)

    def get_aliment_by_id(self, aliment_id: int) -> Aliment:
        try:
            sql = "SELECT name, tags FROM aliment WHERE aliment_id = %s"
            self.cursor.execute(sql, (aliment_id,))
            row = self.cursor.fetchone()
            if row:
                name, tags = row
                return Aliment(name=name, tags=tags, db_id=aliment_id)
            else:
                print("Aliment not found")
        except psycopg2.Error as e:
            print("Error getting aliment by ID:", e)

    def remove_aliment(self, aliment: Aliment):
        try:
            sql = "DELETE FROM aliment WHERE aliment_id = %s"
            self.cursor.execute(sql, (aliment.db_id,))
            self.connection.commit()
            print("Aliment removed successfully")
        except psycopg2.Error as e:
            print("Error removing aliment:", e)

    def update_aliment(self, aliment: Aliment):
        try:
            sql = "UPDATE aliment SET name = %s, tags = %s WHERE aliment_id = %s"
            self.cursor.execute(sql, (aliment.name, aliment.tags, aliment.db_id))
            self.connection.commit()
            print("Aliment updated successfully")
        except psycopg2.Error as e:
            print("Error updating aliment:", e)

    # endregion

    # region CRUD Ingredient
    def add_ingredient(self, ingredient: Ingredient):
        try:
            sql = (
                "INSERT INTO ingredient (aliment_id, quantity, quantity_type, optional) VALUES (%s, %s, %s, %s) RETURNING "
                "ingredient_id"
            )
            self.cursor.execute(
                sql,
                (
                    ingredient.aliment.db_id,
                    ingredient.quantity,
                    ingredient.quantity_type,
                    ingredient.optional,
                ),
            )
            ingredient.set_db_id(self.cursor.fetchone()[0])
            self.connection.commit()
            print("Ingredient added successfully")
        except psycopg2.Error as e:
            print("Error adding ingredient:", e)
            raise e

    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        try:
            sql = "SELECT aliment_id, quantity, quantity_type, optional FROM ingredient WHERE ingredient_id = %s"
            self.cursor.execute(sql, (ingredient_id,))
            row = self.cursor.fetchone()
            if row:
                aliment_id, quantity, quantity_type, optional = row
                aliment = self.get_aliment_by_id(aliment_id)
                return Ingredient(
                    aliment=aliment,
                    quantity=quantity,
                    quantity_type=quantity_type,
                    optional=optional,
                    db_id=ingredient_id,
                )
            else:
                print("Ingredient not found")
        except psycopg2.Error as e:
            print("Error getting ingredient by ID:", e)

    def remove_ingredient(self, ingredient: Ingredient):
        try:
            sql = "DELETE FROM ingredient WHERE ingredient_id = %s"
            self.cursor.execute(sql, (ingredient.db_id,))
            self.connection.commit()
            print("Ingredient removed successfully")
        except psycopg2.Error as e:
            print("Error removing ingredient:", e)

    def update_ingredient(self, ingredient: Ingredient):
        try:
            # Update the aliment if necessary
            self.update_aliment(ingredient.aliment)

            sql = "UPDATE ingredient SET aliment_id = %s, quantity = %s, quantity_type = %s, optional = %s WHERE ingredient_id = %s"
            self.cursor.execute(
                sql,
                (
                    ingredient.aliment.db_id,
                    ingredient.quantity,
                    ingredient.quantity_type,
                    ingredient.optional,
                    ingredient.db_id,
                ),
            )
            self.connection.commit()
            print("Ingredient updated successfully")
        except psycopg2.Error as e:
            print("Error updating ingredient:", e)

    # endregion

    # region CRUD Recipe

    def add_recipe(self, recipe: Recipe):
        try:
            # Add the ingredients and aliments if they don't exist
            for ingredient in recipe.ingredients:
                self.add_ingredient(ingredient)

            sql = (
                "INSERT INTO recipe (name, num_people, steps, category, tags, time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING "
                "recipe_id"
            )
            self.cursor.execute(
                sql,
                (
                    recipe.name,
                    recipe.num_people,
                    recipe.steps,
                    recipe.category,
                    recipe.tags,
                    recipe.time,
                ),
            )
            recipe_id = self.cursor.fetchone()[0]
            recipe.set_db_id(recipe_id)

            for ingredient in recipe.ingredients:
                sql = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (%s, %s)"
                self.cursor.execute(sql, (recipe_id, ingredient.db_id))

            self.connection.commit()
            print("Recipe added successfully")
        except psycopg2.Error as e:
            print("Error adding recipe:", e)
            raise e

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        try:
            sql = "SELECT name, num_people, steps, category, tags, time FROM recipe WHERE recipe_id = %s"
            self.cursor.execute(sql, (recipe_id,))
            row = self.cursor.fetchone()
            if row:
                name, num_people, steps, category, tags, time = row
                # Fetch ingredients of the recipe
                sql = (
                    "SELECT aliment_id, quantity, quantity_type, optional FROM ingredient JOIN recipe_ingredient "
                    "ON ingredient.ingredient_id = recipe_ingredient.ingredient_id WHERE recipe_ingredient.recipe_id = %s"
                )
                self.cursor.execute(sql, (recipe_id,))
                ingredients = [
                    Ingredient(
                        aliment=self.get_aliment_by_id(aliment_id),
                        quantity=quantity,
                        quantity_type=quantity_type,
                        optional=optional,
                    )
                    for aliment_id, quantity, quantity_type, optional in self.cursor.fetchall()
                ]
                return Recipe(
                    name=name,
                    num_people=num_people,
                    ingredients=ingredients,
                    steps=steps,
                    category=category,
                    tags=tags,
                    time=time,
                    db_id=recipe_id,
                )
            else:
                print("Recipe not found")
        except psycopg2.Error as e:
            print("Error getting recipe by ID:", e)

    def remove_recipe(self, recipe: Recipe):
        try:
            sql = "DELETE FROM recipe WHERE recipe_id = %s"
            self.cursor.execute(sql, (recipe.db_id,))
            self.connection.commit()
            print("Recipe removed successfully")
        except psycopg2.Error as e:
            print("Error removing recipe:", e)

    def update_recipe(self, recipe: Recipe):
        try:
            sql = (
                f"DELETE FROM ingredient WHERE ingredient_id IN (SELECT ingredient_id FROM recipe_ingredient"
                f"WHERE recipe_id = {recipe.db_id})"
            )
            self.cursor.execute(sql)

            # Update recipe_ingredient relationships
            sql = "DELETE FROM recipe_ingredient WHERE recipe_id = %s"
            self.cursor.execute(sql, (recipe.db_id,))

            for ingredient in recipe.ingredients:
                self.add_ingredient(ingredient)

            sql = (
                "UPDATE recipe SET name = %s, num_people = %s, steps = %s, category = %s, tags = %s, time = %s "
                "WHERE recipe_id = %s"
            )
            self.cursor.execute(
                sql,
                (
                    recipe.name,
                    recipe.num_people,
                    recipe.steps,
                    recipe.category,
                    recipe.tags,
                    recipe.time,
                    recipe.db_id,
                ),
            )

            for ingredient in recipe.ingredients:
                sql = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (%s, %s)"
                self.cursor.execute(sql, (recipe.db_id, ingredient.db_id))

            self.connection.commit()
            print("Recipe updated successfully")
        except psycopg2.Error as e:
            print("Error updating recipe:", e)

    # endregion

    # region Catalgos

    def get_all_aliments(self) -> List[Aliment]:
        with self.connection.cursor() as cursor:
            aliments = []
            try:
                sql = "SELECT name, tags, aliment_id FROM aliment"
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    name, tags, db_id = row
                    aliments.append(Aliment(name=name, tags=tags, db_id=db_id))
                return aliments
            except psycopg2.Error as e:
                print("Error getting all aliments:", e)
                raise e

    def get_all_recipes(self) -> List[Recipe]:
        recipes = []
        try:
            sql = "SELECT recipe_id, name, num_people, steps, category, tags, time FROM recipe"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for row in rows:
                recipe_id, name, num_people, steps, category, tags, time = row
                # Fetch ingredients of the recipe
                sql = (
                    "SELECT aliment_id, quantity, quantity_type, optional FROM ingredient JOIN recipe_ingredient "
                    "ON ingredient.ingredient_id = recipe_ingredient.ingredient_id WHERE recipe_ingredient.recipe_id = %s"
                )
                self.cursor.execute(sql, (recipe_id,))
                ingredients = [
                    Ingredient(
                        aliment=self.get_aliment_by_id(aliment_id),
                        quantity=quantity,
                        quantity_type=quantity_type,
                        optional=optional,
                    )
                    for aliment_id, quantity, quantity_type, optional in self.cursor.fetchall()
                ]
                recipes.append(
                    Recipe(
                        name=name,
                        num_people=num_people,
                        ingredients=ingredients,
                        steps=steps,
                        category=category,
                        tags=tags,
                        time=time,
                        db_id=recipe_id,
                    )
                )
            return recipes
        except psycopg2.Error as e:
            print("Error getting all recipes:", e)
            return []

    def get_shopping_list(self) -> List[str]:
        shopping_list = []
        try:
            sql = "SELECT item FROM shopping_list"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for row in rows:
                (item,) = row
                shopping_list.append(item)
            return shopping_list
        except psycopg2.Error as e:
            print("Error getting shopping list:", e)
            return []

    def get_pantry(self) -> List[Aliment]:
        pantry = []
        try:
            sql = "SELECT aliment_id FROM pantry"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for row in rows:
                (aliment_id,) = row
                pantry.append(self.get_aliment_by_id(aliment_id))
            return pantry
        except psycopg2.Error as e:
            print("Error getting pantry:", e)
            raise e

    # endregion

    # region Shopping list
    def insert_item_in_shopping_list(self, item: str):
        try:
            sql = "INSERT INTO shopping_list (item) VALUES (%s)"
            self.cursor.execute(sql, (item,))
            self.connection.commit()
            print("Item inserted into shopping list successfully")
        except psycopg2.Error as e:
            print("Error inserting item into shopping list:", e)

    def remove_item_in_shopping_list(self, item: str):
        try:
            sql = "DELETE FROM shopping_list WHERE item = %s"
            self.cursor.execute(sql, (item,))
            self.connection.commit()
            print("Item removed from shopping list successfully")
        except psycopg2.Error as e:
            print("Error removing item from shopping list:", e)

    # endregion

    # region Pantry
    def add_aliment_to_pantry(self, aliment: Aliment):
        try:
            sql = "INSERT INTO pantry (aliment_id) VALUES (%s)"
            self.cursor.execute(sql, (aliment.db_id,))
            self.connection.commit()
            print("Aliment added to pantry successfully")
        except psycopg2.Error as e:
            print("Error adding aliment to pantry:", e)

    def remove_aliment_from_pantry(self, aliment: Aliment):
        try:
            sql = "DELETE FROM pantry WHERE aliment_id = %s"
            self.cursor.execute(sql, (aliment.db_id,))
            self.connection.commit()
            print("Aliment removed from pantry successfully")
        except psycopg2.Error as e:
            print("Error removing aliment from pantry:", e)

    # endregion

    def execute(self, sql: str):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error executing SQL query:", e, "\n", sql)

    def query(self, sql: str) -> List[str]:
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            result = [str(row) for row in rows]
            return result
        except psycopg2.Error as e:
            print("Error executing SQL query:", e, "\n", sql)
            return []
