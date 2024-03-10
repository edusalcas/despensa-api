from despensa.abstract_connector import AbstractConnector
from despensa.singleton_meta import WeakSingletonMeta


class ShoppingList(metaclass=WeakSingletonMeta):
    def __init__(self, db_connector: AbstractConnector):
        self.db_connector: AbstractConnector = db_connector
        self.__shopping_list: list[str] = db_connector.get_shopping_list()

    def is_present(self, item: str) -> bool:
        return item in self.__shopping_list

    def add_item_to_shopping_list(self, item: str) -> bool:
        if not self.is_present(item):
            self.db_connector.insert_item_in_shopping_list(item)
            self.__shopping_list.append(item)
            return True

        return False

    def get_all(self) -> list[str]:
        return self.__shopping_list.copy()

    def remove_item_from_shopping_list(self, name: str):
        if self.is_present(name):
            self.__shopping_list.remove(name)
            self.db_connector.remove_item_in_shopping_list(name)
