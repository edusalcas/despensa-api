from typing import List, Union

from despensa.classes import Aliment
from despensa.singleton_meta import SingletonMeta
from despensa.sqlite_connector import SQLiteConnector


class Pantry(metaclass=SingletonMeta):
    def __init__(self, db_connector: SQLiteConnector):
        self.db_connector: SQLiteConnector = db_connector
        self.__pantry_list: list[Aliment] = db_connector.get_pantry()
        self.__aliment_name_map: dict[str, Aliment] = dict(zip([a.name for a in self.__pantry_list], self.__pantry_list))

    def is_present(self, aliment: Aliment) -> bool:
        return aliment in self.__pantry_list

    def add_aliment_to_pantry(self, aliment: Aliment) -> bool:
        if aliment not in self.__pantry_list:
            self.db_connector.add_ingredient_to_pantry(aliment)
            self.__pantry_list.append(aliment)
            return True

        return False

    def remove_aliment_from_pantry(self, name: str):
        self.__aliment_name_map.pop(name, None)

    def get_all(self) -> list[Aliment]:
        return self.__pantry_list.copy()


