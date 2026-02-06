from abc import ABC, abstractmethod
from typing import Any


class BDInstance(ABC):
    """Class with implements the db_id for objects who will be in database"""

    def __init__(self):
        self.db_id = None

    def set_db_id(self, db_id: int):
        """Set the id of the aliment in the database

        :param db_id: id of the aliment in the database
        """
        self.db_id = db_id

    @staticmethod
    @abstractmethod
    def from_json(json: dict[str, Any]) -> "BDInstance": ...
