from dataclasses import dataclass, field
from enum import Enum


class AlimentType(Enum):
    """Class which represents the types of the aliments"""
    MEAT = 1
    FISH = 2
    VEGETABLE = 3
    FRUIT = 4
    OIL = 5


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
    type: AlimentType


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


def main():
    ingredients = []
    aliments = {
        'olive oil': Aliment("Olive oil", AlimentType.OIL),
        'garlic': Aliment("Garlic", AlimentType.VEGETABLE),
        'onion': Aliment("Onion", AlimentType.VEGETABLE),
        'ginger': Aliment("Ginger", AlimentType.VEGETABLE),
    }

    ingredients.append(Ingredient(aliments['olive oil'], 1, 'spoon', True))
    ingredients.append(Ingredient(aliments['garlic'], 2, 'cloves'))
    ingredients.append(Ingredient(aliments['onion'], 1/2, ''))
    ingredients.append(Ingredient(aliments['ginger'], 2.5, 'cm'))

    steps = [
        "Calienta el aceite en una sartén y añade los ajos, la cebolla y el jengibre. Cocina a fuego medio-alto "
        "durante unos 5 ó 10 minutos o hasta que se doren, removiendo de vez en cuando. Si no quieres usar aceite, "
        "puede sustituirlo por un poco de agua o caldo de verduras.",
        "Añade las especias (curry, comino, cúrcuma, semillas de cilantro, pimienta y cayena), remueve y cocina 1 ó 2 "
        "minutos más.",
        "Añade los garbanzos, la leche de coco, el concentrado de tomate y la sal. Remueve y cocina a fuego "
        "medio-alto durante unos 10 minutos.",
        "Retira del fuego y añade el zumo de lima y la cucharada de harina de coco, remueve y deja reposar unos 5 "
        "minutos antes de servir.",
        "Sirve inmediatamente (yo le añadí un poco de cilantro fresco troceado por encima). Está muy rico con arroz, "
        "pan naan y pan pita. Guarda las sobras en la nevera en un recipiente hermético durante unos 5-7 días.",
    ]

    curry_de_garbanzos = Recipe("Curry de garbanzos", 4, ingredients, steps, category='Main', tags=['Vegana', "India"], time=30)

    print(curry_de_garbanzos)

if __name__ == "__main__":
    main()
