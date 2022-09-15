from classes import Aliment
import view_console
from typing import List


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Controller(metaclass=Singleton):
    __aliments_catalog = []

    def __init__(self):
        self.view = view_console.ConsoleView()

    def start(self):
        self.view.run()

    def insert_aliment(self, name: str, tags: List[str]) -> bool:
        aliment = Aliment(name, tags)
        if aliment in self.__aliments_catalog:  # Aliment already exists
            return False

        self.__aliments_catalog.append(aliment)
        return True

    def update_aliment(self, name, tags):
        aliment = Aliment(name, tags)
        if aliment in self.__aliments_catalog:  # Aliment already exists
            self.__aliments_catalog.remove(aliment)

        self.__aliments_catalog.append(aliment)

    def get_aliments(self):
        return self.__aliments_catalog


unique_instance = None


def get_unique_instance() -> Controller:
    global unique_instance

    if unique_instance is None:
        unique_instance = Controller()
    return unique_instance
