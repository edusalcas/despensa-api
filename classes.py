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
    tags: str = field(default_factory=list)


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
