import os
import controller
from classes import Ingredient


def clear_console():
    os.system('cls')


def bool_y_n(condition: str):
    return condition == 'Y'


class ConsoleView():

    def insert_aliment(self):
        name = input("Aliment's name: ")
        tags_str = input("Aliment's tags: ")

        try:
            tags = tags_str.strip().split(' ')
        except Exception as e:
            print(e)
            return

        exists = not controller.get_unique_instance().insert_aliment(name, tags)

        if exists:
            override = input("An aliment with the same name already exists, do you want to override it? (Y/N): ")
            if bool_y_n(override):
                controller.get_unique_instance().update_aliment(name, tags)

    def create_ingredient(self) -> Ingredient or None:
        aliments_name = input("\tAliment's name: ")
        quantity_str = input("\tQuantity: ")
        quantity_type = input("\tQuantity's type: ")
        optional_str = input("\tIs optional? (Y/N): ")

        try:
            quantity = float(quantity_str)
            optional = bool_y_n(optional_str)
        except Exception as e:
            print(e)
            return None

        return controller.get_unique_instance().create_ingredient(aliments_name, quantity, quantity_type, optional)

    def insert_recipe(self):
        recipe_name = input("1. Insert recipe's name: ")
        num_people_str = input("2. Insert num people: ")
        category = input("3. Insert recipe's category: ")
        time_str = input("4. Insert recipe's time (minutes): ")

        ingredients = []
        print("5. Insert ingredients:")
        while True:
            ingredient = self.create_ingredient()

            if ingredient is None:
                print(f'\tAliment does not exists, insert it first.')
            else:
                ingredients.append(ingredient)

            condition = input('\n\tInsert another ingredient? (Y/N): ')
            if not bool_y_n(condition):
                break

        tags_str = input("6. Insert tags: ")
        try:
            tags = tags_str.strip().split(' ')
        except Exception as e:
            print(e)
            return

        steps = []
        i = 1
        print("5. Insert steps:")
        while True:
            step = input(f'\t Step {i}: ')
            if step == '':
                break
            steps.append(step)

            i += 1

        try:
            num_people = int(num_people_str)
            time = int(time_str)
        except Exception as e:
            print(e)
            return None

        recipe = controller.get_unique_instance().create_recipe(recipe_name, num_people, ingredients, steps, category, tags, time)

        clear_console()
        print("Your recipe is:\n")
        print(recipe)
        input("\nIs it okay?")

        controller.get_unique_instance().insert_recipe(recipe)

    def run(self):
        print("Press:")
        print("\t1. Create recipe.")
        print("\t2. Create aliment.")
        print("\t3. List aliments.")
        print("\t4. List recipes.")

        action = input()

        if action == '1':
            clear_console()
            self.insert_recipe()
            clear_console()
            self.run()
        elif action == '2':
            clear_console()
            self.insert_aliment()
            clear_console()
            self.run()
        elif action == '3':
            clear_console()
            aliments = controller.get_unique_instance().get_aliments_catalog()
            print(aliments)
            input()
            clear_console()
            self.run()
        elif action == '4':
            clear_console()
            recipes = controller.get_unique_instance().get_recipes_catalog()
            print(recipes)
            input()
            clear_console()
            self.run()
        else:
            clear_console()
            input('Input error, press enter to try again...')
            clear_console()

