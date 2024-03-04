from typing import List, Union

from despensa.classes import Aliment
from despensa.singleton_meta import WeakSingletonMeta
from despensa.sqlite_connector import SQLiteConnector


class AlimentCatalog(metaclass=WeakSingletonMeta):
    def __init__(self, db_connector: SQLiteConnector):
        self.db_connector: SQLiteConnector = db_connector
        self.__aliment_list: list[Aliment] = db_connector.get_all_aliments()
        self.__aliment_id_map: dict[int, Aliment] = dict(
            zip([a.db_id for a in self.__aliment_list], self.__aliment_list))
        self.__aliment_name_map: dict[str, Aliment] = dict(
            zip([a.name for a in self.__aliment_list], self.__aliment_list))

    def is_present(self, aliment: Aliment) -> bool:
        return aliment in self.__aliment_list

    def get_aliment_by_name(self, name: str) -> Union[Aliment, None]:
        return self.__aliment_name_map.get(name)

    def get_aliment_by_id(self, bd_id: int) -> Union[Aliment, None]:
        return self.__aliment_id_map.get(bd_id)

    def create_aliment_from_params(self, name: str, tags: List[str]) -> bool:
        aliment = Aliment(name.lower(), tags)
        return self.create_aliment(aliment)

    def create_aliment(self, aliment: Aliment):
        if self.is_present(aliment):
            return False
        self.db_connector.add_aliment(aliment)
        self.__aliment_list.append(aliment)
        self.__aliment_id_map[aliment.db_id] = aliment
        return True

    def create_aliment_from_json(self, json: dict) -> bool:
        aliment: Aliment = Aliment.from_json(json)
        return self.create_aliment(aliment)

    def update_aliment(self, name, tags):
        aliment = self.get_aliment_by_name(name)
        if aliment:
            aliment.tags = tags
            self.db_connector.update_aliment(aliment)

    def update_aliment_from_json(self, id_aliment: int, json: dict):
        aliment = self.get_aliment_by_id(id_aliment)
        if aliment:
            aliment = aliment.update_from_json(json)
            self.db_connector.update_aliment(aliment)

    def get_all(self) -> list[Aliment]:
        return self.__aliment_list.copy()

    def delete_aliment(self, id_aliment: int):
        aliment = self.get_aliment_by_id(id_aliment)
        self.__aliment_list.remove(aliment)
        self.__aliment_id_map.pop(id_aliment)
        self.__aliment_name_map.pop(aliment.name)
        self.db_connector.delete_aliment(id_aliment)
