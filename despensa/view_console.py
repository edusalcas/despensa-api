from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List

import despensa.controller as controller
from despensa.classes import Ingredient

import os


def clear_console():
    os.system('cls')


def bool_y_n(condition: str):
    return condition == 'Y'


class ConsoleView:
    @dataclass
    class Option:
        info: str
        action: Callable[[ConsoleView], None]

    def create_aliment(self) -> None:
        name = input("Aliment's name: ")
        tags_str = input("Aliment's tags: ")

        try:
            tags = tags_str.strip().split(' ')
        except Exception as e:
            print(e)
            return

        if not controller.get_unique_instance().create_aliment(name, tags):
            override = input("An aliment with the same name already exists, do you want to override it? (Y/N): ")
            if bool_y_n(override):
                controller.get_unique_instance().update_aliment(name, tags)

    def create_ingredients(self) -> List[Ingredient]:
        ingredients = []
        while True:
            aliments_name = input("\tAliment's name: ")
            quantity = float(input("\tQuantity: "))
            quantity_type = input("\tQuantity's type: ")
            optional = bool_y_n(input("\tIs optional? (Y/N): "))

            ingredient = controller.get_unique_instance().create_ingredient(aliments_name, quantity, quantity_type,
                                                                            optional)
            if ingredient is None:
                print(f'\tAliment does not exists, insert it first.')
            else:
                ingredients.append(ingredient)

            condition = input('\n\tInsert another ingredient? (Y/N): ')
            if not bool_y_n(condition):
                break
        return ingredients

    def get_steps(self) -> List[str]:
        steps = []
        i = 1
        while True:
            step = input(f'\t Step {i}: ')
            if step == '':
                break
            steps.append(step)
            i += 1

        return steps

    def create_recipe(self) -> None:
        recipe_name = input("1. Insert recipe's name: ")
        num_people = int(input("2. Insert num people: "))
        category = input("3. Insert recipe's category: ")
        time = int(input("4. Insert recipe's time (minutes): "))
        print("5. Insert ingredients:")
        ingredients = self.create_ingredients()

        tags = input("6. Insert tags: ").strip().split(' ')

        print("7. Insert steps:")
        steps = self.get_steps()

        recipe = controller.get_unique_instance().create_recipe(recipe_name, num_people, ingredients, steps, category,
                                                                tags, time)

        clear_console()
        print("Your recipe is:\n")
        print(recipe)
        res = input("\nIs it okay?")
        if bool_y_n(res):
            controller.get_unique_instance().insert_recipe(recipe)

    def insert_aliment_in_pantry(self):
        name = input("Aliment's name: ")
        if controller.get_unique_instance().insert_aliment_in_pantry(name) == -1:
            input(f"Error: Aliment '{name}' does not exists. Please, create it before trying to insert it into the "
                  f"pantry.")

    def remove_aliment_in_pantry(self):
        name = input("Aliment's name: ")
        controller.get_unique_instance().remove_aliment_in_pantry(name)

    def list_pantry(self):
        pantry = controller.get_unique_instance().get_pantry()
        if pantry:
            print('\n'.join([a.simple_str() for a in pantry]))
        else:
            print('Empty pantry.')
        input()

    def list_recipes_catalog(self):
        recipes = controller.get_unique_instance().get_recipes_catalog()
        print('\n'.join([r.simple_str() for r in recipes]))
        recipe_name = input('\nRecipe to inspect:')

        for recipe in recipes:
            if recipe.name.lower() == recipe_name.lower():
                print(recipe)
                print("""
    Press:
        1. Edit
        2. Remove
        3. Add aliments to shopping list
        
        q. Exit
                """)

                input()  # TODO: Add options functionality

    def list_aliments_catalog(self):
        aliments = controller.get_unique_instance().get_aliments_catalog()
        print('\n'.join([a.simple_str() for a in aliments]))
        input()

    def get_recipes_from_pantry(self):
        recipes = controller.get_unique_instance().get_recipes_from_pantry()
        print('\n'.join([str(r) for r in recipes]))
        input()

    def insert_item_in_shopping_list(self):
        item = input("Item's name: ")
        controller.get_unique_instance().insert_item_in_shopping_list(item)

    def get_shopping_list(self):
        shopping_list = controller.get_unique_instance().get_shopping_list()
        print('\n'.join([str(r) for r in shopping_list]))
        input()

    __LIST_ALIMENT: int = 1
    __LIST_RECIPES: int = 2
    __CREATE_RECIPE: int = 3
    __CREATE_ALIMENT: int = 4
    __LIST_PANTRY: int = 5
    __INSERT_ALIMENT_PANTRY: int = 6
    __REMOVE_ALIMENT_PANTRY: int = 7
    __GET_RECIPES_PANTRY: int = 8
    __INSERT_ALIMENT_SHOPPING_LIST: int = 9
    __GET_SHOPPING_LIST: int = 10
    __EXIT: str = 'q'

    __DICT_OPTIONS: dict[int, Option] = {
        __LIST_ALIMENT: Option('Create aliment', create_aliment),
        __LIST_RECIPES: Option('Create recipe', create_recipe),
        __CREATE_RECIPE: Option('List aliments', list_aliments_catalog),
        __CREATE_ALIMENT: Option('List recipes', list_recipes_catalog),
        __LIST_PANTRY: Option('Show pantry', list_pantry),
        __INSERT_ALIMENT_PANTRY: Option('Insert aliment in pantry', insert_aliment_in_pantry),
        __REMOVE_ALIMENT_PANTRY: Option('Remove aliment from pantry', remove_aliment_in_pantry),
        __GET_RECIPES_PANTRY: Option('Get doable recipes with pantry', get_recipes_from_pantry),
        __INSERT_ALIMENT_SHOPPING_LIST: Option('Insert aliment to the shopping list', insert_item_in_shopping_list),
        __GET_SHOPPING_LIST: Option('Get shopping list', get_shopping_list),
    }

    def print_options(self):
        print("Press:")
        for key, option in self.__DICT_OPTIONS.items():
            print(f"\t{key}. {option.info}.")
        print()
        print(f"Press '{self.__EXIT}' to exit.")

    def run(self):
        while True:
            self.print_options()

            key = input()

            clear_console()
            if key.isdigit():
                if int(key) in self.__DICT_OPTIONS:
                    self.__DICT_OPTIONS[int(key)].action(self)
            elif key == self.__EXIT:
                break
            else:
                input('Input error, press enter to try again...')
            clear_console()
