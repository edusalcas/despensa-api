from dataclasses import dataclass, field
from typing import Any
from despensa.objects.bd_instance import BDInstance


@dataclass
class Aliment(BDInstance):
    """Class which represents an aliment

     Attributes
    ----------
    name : str
        the name of the aliment
    tags : list[str]
        list of tags for the aliment
    """

    name: str
    tags: list[str] = field(default_factory=list)
    db_id: int = 0

    def __post_init__(self):
        self.name = self.name.lower().strip()
        self.tags = [" ".join(tag.lower().split()) for tag in self.tags]

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, type(self)):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def simple_str(self) -> str:
        """Returns a simplified str of the aliment

        :return: Simple description of the aliment
        """
        return f"{self.name.title()}: {', '.join(map(str.title, self.tags))}"

    def update_from_json(self, json: dict) -> "Aliment":
        self.name = json["name"]
        self.tags = json["tags"]

        return self

    @staticmethod
    def from_json(json: dict[str, Any]) -> "Aliment":
        return Aliment(json["name"], json.get("tags", []), json.get("db_id", 0))
