from dataclasses import dataclass
from typing import Any

from despensa.objects.aliment import Aliment
from despensa.objects.bd_instance import BDInstance


@dataclass
class Ingredient(BDInstance):
    """Class which represents an ingredient: an aliment for a recipe with a quantity

     Attributes
    ----------
    aliment : Aliment
        the concrete aliment
    quantity : int
        quantity of the aliment for a recipe
    quantity_type : str
        the type of the quantity. f.e. "gr", "kg", "spoons"...
    """

    aliment: Aliment
    quantity: float
    quantity_type: str = ""
    optional: bool = False
    db_id: int = 0

    def simple_str(self) -> str:
        """Returns a simplified str of the ingredient

        :return: Simple description of the ingredient
        """
        return f"{self.aliment.name.title()}: {self.quantity} {self.quantity_type}" + (
            " (Optional)" if self.optional else ""
        )

    @staticmethod
    def from_json(json: dict[str, Any]) -> "Ingredient":
        return Ingredient(
            Aliment.from_json(json["aliment"]),
            json["quantity"],
            json["quantity_type"],
            json["optional"],
            json["db_id"],
        )

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Ingredient):
            return (
                self.aliment == other.aliment
                and self.quantity == other.quantity
                and self.quantity_type == other.quantity_type
                and self.optional == other.optional
            )
        return False
