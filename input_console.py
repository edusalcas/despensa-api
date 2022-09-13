import os


def clear_console():
    os.system('cls')


class ConsoleInput():

    def insert_recipe(self):
        print("1. Insert recipe name: ", end='')
        name = input()
        print("2. Insert num people: ", end='')
        num_people = input()
        print("3. Insert recipe category: ", end='')
        category = input()
        print("4. Insert recipe time (minutes): ", end='')
        time = input()
        print("5. Insert ingredients:")
        while True:
            sample = input()
            if sample == '':
                break
        print("6. Insert ...")
        input()
        input("Is it okay?")


    def run(self):
        print("Press:")
        print("\t1. Insert recipe.")
        print("\t2. Insert aliment.")

        action = input()

        if action == '1':
            clear_console()
            self.insert_recipe()
            clear_console()
            self.run()
        elif action == '2':
            clear_console()
            print(2)
        else:
            clear_console()
            input('Input error, press enter to try again...')
            clear_console()
