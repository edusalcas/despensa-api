import os
import controller


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

    def insert_ingredient(self):
        name = input("\tAliment's name: ")
        quantity = input("\tQuantity: ")
        quantity_type = input("\tQuantity's type: ")
        optional = input("\tIs optional? (Y/N): ")

    def insert_recipe(self):
        name = input("1. Insert recipe's name: ")
        num_people = input("2. Insert num people: ")
        category = input("3. Insert recipe's category: ")
        time = input("4. Insert recipe's time (minutes): ")
        print("5. Insert ingredients:")
        while True:
            self.insert_ingredient()

            condition = input('\tInsert another ingredient? (Y/N): ')
            if not bool_y_n(condition):
                break
        print("6. Insert ...")
        input()
        input("Is it okay?")

    def run(self):
        print("Press:")
        print("\t1. Insert recipe.")
        print("\t2. Insert aliment.")
        print("\t3. List aliments.")

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
            aliments = controller.get_unique_instance().get_aliments()
            print(aliments)
            input()
            clear_console()
            self.run()
        else:
            clear_console()
            input('Input error, press enter to try again...')
            clear_console()

