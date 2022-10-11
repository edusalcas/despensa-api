from despensa.classes import Aliment, Ingredient, Recipe
import despensa.view_console as view_console
from despensa.singleton import Singleton

import despensa.sqlite_connector as sqlite

from typing import List


class Controller(metaclass=Singleton):
    """Class controller for separate the UI and the functionality"""
    __aliments_catalog: list[Aliment] = []
    __recipes_catalog: list[Recipe] = []
    __pantry: list[Aliment] = []

    def __init__(self):
        # Create the view
        self.view = view_console.ConsoleView()

    def init_catalogs(self):
        """Init the catalogs from the database"""
        # Recuperate the catalogs from the database
        self.__aliments_catalog = sqlite.get_unique_instance().get_all_aliments()
        self.__recipes_catalog = sqlite.get_unique_instance().get_all_recipes()
        self.__pantry = sqlite.get_unique_instance().get_pantry()

    def start(self):
        """Start the UI"""
        self.view.run()

    def create_aliment(self, name: str, tags: List[str]) -> bool:
        """Insert an aliment, if it already exists, returns False

        :param name: Name of the aliment
        :param tags: Tags of the aliment
        :return: True if inserted, False if the aliment already exists
        """
        aliment = Aliment(name.lower(), tags)
        if aliment in self.__aliments_catalog:  # Aliment already exists
            return False

        sqlite.get_unique_instance().add_aliment(aliment)
        self.__aliments_catalog.append(aliment)
        return True

    def insert_aliment_in_pantry(self, name: str) -> int:
        """Inserts an already existing aliment into the pantry

        :param name: Name of the existing aliment
        :return: -1 if aliment does not exist 0 otherwise
        """
        for aliment in self.__aliments_catalog:
            if aliment.name == name.lower().strip():
                if aliment not in self.__pantry:
                    self.__pantry.append(aliment)
                    sqlite.get_unique_instance().add_ingredient_to_pantry(aliment)
                    return 0

        return -1

    def remove_aliment_in_pantry(self, name: str) -> None:
        """Remove an aliment from pantry

        :param name: Aliment's name
        """
        for aliment in self.__pantry:
            if aliment.name == name.lower().strip():
                self.__pantry.remove(aliment)
                sqlite.get_unique_instance().remove_ingredient_from_pantry(aliment)
                return

    def update_aliment(self, name: str, tags: List[str]):
        """Update an aliment

        :param name: Name of the aliment
        :param tags: Tags of the aliment
        """
        aliment = Aliment(name.lower(), tags)
        if aliment in self.__aliments_catalog:  # Aliment already exists
            self.__aliments_catalog.remove(aliment)

        self.__aliments_catalog.append(aliment)

    def create_ingredient(self, aliments_name: str, quantity: float, quantity_type: str,
                          optional: bool) -> Ingredient or None:
        """Creates an ingredient if aliment exists

        :param aliments_name: Aliment's name
        :param quantity: Quantity of the aliment
        :param quantity_type: Type of the quantity (gr, ounces, spoons...)
        :param optional: If the ingredient is optional or not
        :return: Returns an ingredient if aliment exists, else None
        """
        aliment = self.get_aliment_by_name(aliments_name)
        if aliment is None:
            return None

        ingredient = Ingredient(aliment, quantity, quantity_type, optional)
        return ingredient

    @staticmethod
    def create_recipe(recipe_name: str, num_people: int, ingredients: List[Ingredient], steps: List[str],
                      category: str, tags: List[str], time: int) -> Recipe:
        """

        :param recipe_name:
        :param num_people:
        :param ingredients:
        :param steps:
        :param category:
        :param tags:
        :param time:
        """

        recipe = Recipe(recipe_name, num_people, ingredients, steps, category, tags, time)

        return recipe

    def insert_recipe(self, recipe: Recipe):
        """Insert a recipe in his catalog

        :param recipe: Recipe to insert in catalog
        """
        sqlite.get_unique_instance().add_recipe_and_ingredients(recipe)
        self.__recipes_catalog.append(recipe)

    def get_recipes_from_pantry(self) -> List[Recipe]:
        """Get the recipes which are doable with aliments in pantry

        :return: Return the doable recipes with aliments in pantry
        """
        return [recipe for recipe in self.__recipes_catalog
                if set(recipe.get_not_optional_aliments()) <= set(self.__pantry)]


    #####################################
    #              Getters              #
    #####################################

    def get_aliment_by_name(self, aliment_name: str) -> Aliment or None:
        """Get the aliment from a name if exists

        :param aliment_name: The name of the aliment
        :return: The aliment if it exists, else None
        """
        for aliment in self.__aliments_catalog:
            if aliment.name == aliment_name.lower():
                return aliment

        return None

    def get_aliment_by_id(self, aliment_id: int) -> Aliment or None:
        """Get the aliment from a database id if exists

        :param aliment_id: The id of the aliment in the db
        :return: The aliment if it exists, else None
        """
        for aliment in self.__aliments_catalog:
            if aliment.db_id == aliment_id:
                return aliment

        return None

    def get_aliments_catalog(self) -> List[Aliment]:
        """ Get the list of aliments

        :return: Returns the list of aliments
        """
        return self.__aliments_catalog

    def get_recipes_catalog(self) -> List[Recipe]:
        """ Get the list of recipes

        :return: Returns the list of recipes
        """
        return self.__recipes_catalog

    def get_pantry(self) -> List[Aliment]:
        """ Get the list of aliments in the pantry

        :return: Returns the list of aliments in the pantry
        """
        return self.__pantry


unique_instance = None


def get_unique_instance() -> Controller:
    """This function ensures there is only one instance of the Controller class

    :return: The unique instance of the Controller
    """
    global unique_instance

    if unique_instance is None:
        unique_instance = Controller()
    return unique_instance
