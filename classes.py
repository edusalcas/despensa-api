from dataclasses import dataclass, field


@dataclass
class Aliment:
    """Class which represents an aliment

     Attributes
    ----------
    name : str
        the name of the aliment
    type : AlimentType
        the type of the aliment of AlimentType
    """
    name: str
    tags: list[str] = field(default_factory=list)

    bd_id: int = 0

    def set_bd_id(self, bd_id: int):
        """Set the id of the aliment in the database

        :param bd_id: id of the aliment in the database
        """
        self.bd_id = bd_id

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Aliment):
            return self.name == other.name
        return False


@dataclass
class Ingredient:
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
    quantity_type: str
    optional: bool = False

    bd_id: int = 0

    def set_bd_id(self, bd_id: int):
        """Set the id of the ingredient in the database

        :param bd_id: id of the ingredient in the database
        """
        self.bd_id = bd_id


@dataclass
class Recipe:
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
        the category of the recipe (f.e. main, breakfast...)
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

    bd_id: int = 0

    def set_bd_id(self, bd_id):
        """Set the id of the recipe in the database

        :param bd_id: id of the recipe in the database
        """
        self.bd_id = bd_id
