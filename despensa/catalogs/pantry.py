from typing import Union, List

from despensa.abstract_connector import AbstractConnector
from despensa.catalogs.aliment_catalog import AlimentCatalog
from despensa.classes import Aliment
from despensa.singleton_meta import WeakSingletonMeta


class Pantry(metaclass=WeakSingletonMeta):
    def __init__(self, db_connector: AbstractConnector):
        self.__db_connector: AbstractConnector = db_connector
        with self.__db_connector() as connector:
            self.__pantry_list: list[Aliment] = connector.get_pantry()
        self.__aliment_name_map: dict[str, Aliment] = dict(zip([a.name for a in self.__pantry_list], self.__pantry_list))

    def is_present(self, aliment: Aliment) -> bool:
        return aliment in self.__pantry_list

    def add_aliment_to_pantry(self, aliment_name: str) -> List[Aliment]:
        aliment = AlimentCatalog(self.__db_connector).get_aliment_by_name(aliment_name)

        if aliment and aliment not in self.__pantry_list:
            with self.__db_connector() as connector:
                connector.add_aliment_to_pantry(aliment)
            self.__pantry_list.append(aliment)
            return self.__pantry_list

        raise Exception('Aliment is already in pantry')

    def get_aliment(self, name: str) -> Union[Aliment, None]:
        return self.__aliment_name_map.get(name, None)

    def remove_aliment_from_pantry(self, name: str):
        aliment_to_remove = self.get_aliment(name)
        if aliment_to_remove:
            with self.__db_connector() as connector:
                connector.remove_aliment_from_pantry(aliment_to_remove)
            self.__pantry_list.remove(aliment_to_remove)
            self.__aliment_name_map.pop(name)

    def get_all(self) -> list[Aliment]:
        return self.__pantry_list.copy()


