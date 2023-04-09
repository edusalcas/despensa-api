from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Any
from abc import ABC, abstractmethod


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
    def from_json(json: dict[str, Any]) -> BDInstance:
        ...


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

    def update_from_json(self, json: dict) -> Aliment:
        self.name = json['name']
        self.tags = json['tags']

        return self

    @staticmethod
    def from_json(json: dict[str, Any]) -> Aliment:
        return Aliment(
            json['name'],
            json['tags'],
            json['db_id']
        )


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
    quantity_type: str = ''
    optional: bool = False
    db_id: int = 0

    def simple_str(self) -> str:
        """Returns a simplified str of the ingredient

        :return: Simple description of the ingredient
        """
        return f"{self.aliment.name.title()}: {self.quantity} {self.quantity_type}" + \
               (" (Optional)" if self.optional else "")

    @staticmethod
    def from_json(json: dict[str, Any]) -> Ingredient:
        return Ingredient(
            Aliment.from_json(json['aliment']),
            json['quantity'],
            json['quantity_type'],
            json['optional'],
            json['db_id']
        )

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Ingredient):
            return self.aliment == other.aliment \
                   and self.quantity == other.quantity \
                   and self.quantity_type == other.quantity_type \
                   and self.optional == other.optional
        return False

@dataclass
class Recipe(BDInstance):
    """Class which represents a recipe

     Attributes
    ----------
    name : str
        the name of the aliment
    num_people : int
        the type of the aliment of AlimentType
    ingredients : list[Ingredient]
        the type of the aliment of AlimentType
    steps : list[str]
        the type of the aliment of AlimentType
    category : str
        the category of the recipe (f.e. despensa, breakfast...)
    tags : list[str]
        the type of the aliment of AlimentType
    time : int
        the type of the aliment of AlimentType
    """

    name: str
    num_people: int
    ingredients: list[Ingredient]
    steps: list[str]
    category: str
    tags: list[str] = field(default_factory=list)
    time: int = None
    db_id: int = 0

    def __post_init__(self):
        self.name = " ".join(self.name.split())
        self.steps = [" ".join(step.split()) for step in self.steps]
        self.category = " ".join(self.category.lower().split())
        self.tags = [" ".join(tag.lower().split()) for tag in self.tags]

    def __str__(self) -> str:
        ingredients = '\n\t\t'.join([i.simple_str() for i in self.ingredients])
        recipe_str = f"""\
    Recipe name: {self.name}
        Category: {self.category.title()}
        Tags: {', '.join(map(str.title, self.tags))}
        Number of people: {self.num_people}
        Estimated time: {self.time}

        Ingredients: 
                {ingredients}
        """

        return recipe_str

    def simple_str(self) -> str:
        """Returns a simplified str of the recipe

        :return: Simple description of the recipe
        """
        return f"{self.name} ({self.category.title()}): {', '.join(map(str.title, self.tags))}"

    def get_not_optional_aliments(self) -> List[Aliment]:
        """Get the not optional aliments from the recipe

        :return: Return a list with the non-optional aliments
        """
        return [ingredient.aliment for ingredient in self.ingredients if not ingredient.optional]

    @staticmethod
    def from_json(json: dict[str, Any]) -> Recipe:
        return Recipe(
            json['name'],
            json['num_people'],
            [Ingredient.from_json(ingredient) for ingredient in json['ingredients']],
            json['steps'],
            json['category'],
            json['tags'],
            json['time'],
            json['db_id']
        )

    def update_from_json(self, json: dict) -> Recipe:
        self.name = json['name']
        self.num_people = json['num_people']
        self.ingredients = [Ingredient.from_json(ingredient) for ingredient in json['ingredients']]
        self.steps = json['steps']
        self.tags = json['tags']
        self.time = json['time']

        return self

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Recipe):
            return self.name == other.name \
                   and self.num_people == other.num_people \
                   and self.ingredients == other.ingredients \
                   and self.steps == other.steps \
                   and self.tags == other.tags \
                   and self.time == other.time
        return False
