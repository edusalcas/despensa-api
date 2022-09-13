from classes import *
from input_console import ConsoleInput

def main_maual():
    ingredients = []
    aliments = {
        'olive oil': Aliment("Olive oil", ["Oil"]),
        'garlic': Aliment("Garlic", ["Vegetable"]),
        'onion': Aliment("Onion", ["Vegetable"]),
        'ginger': Aliment("Ginger", ["Vegetable"]),
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

def main():
    ci = ConsoleInput()
    ci.run()


if __name__ == "__main__":
    main()
