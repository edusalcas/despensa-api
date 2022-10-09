from dataclasses import dataclass, field


class BDInstance():

    def __init__(self):
        self.db_id = None

    def set_db_id(self, db_id: int):
        """Set the id of the aliment in the database

        :param db_id: id of the aliment in the database
        """
        self.db_id = db_id


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
        if isinstance(other, Aliment):
            return self.name == other.name
        return False


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
    db_id: int = 0

    def __post_init__(self):
        self.name = " ".join(self.name.split())
        self.steps = [" ".join(step.split()) for step in self.steps]
        self.category = " ".join(self.category.lower().split())
        self.tags = [" ".join(tag.lower().split()) for tag in self.tags]
