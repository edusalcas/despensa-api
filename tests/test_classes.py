from despensa.classes import Aliment, Ingredient, Recipe
from environment import Environment

Environment().working_is_test()


class TestAliment:
    def test_aliment_only_name_created(self):
        al = Aliment(name='Onion Juice ')
        assert al.name == 'onion juice' and al.tags == []

    def test_aliment_name_and_tags_created(self):
        al = Aliment(name='onion ', tags=['VEGETABLE', 'Healthy', 'vitamin  C'])
        assert al.name == 'onion' and al.tags == ['vegetable', 'healthy', 'vitamin c']

    def test_aliments_equal(self):
        al1 = Aliment(name='Onion', tags=['vegetable'])
        al2 = Aliment(name='onion')
        assert al1 == al2

    def test_aliment_not_equal(self):
        al1 = Aliment(name='Onion', tags=['vegetable'])
        al2 = Aliment(name='onion juice', tags=['juice'])
        assert al1 != al2

    def test_aliment_simple_str(self):
        al = Aliment(name='onion', tags=['VEGETABLE', 'Healthy', 'vitamin C'])

        assert al.simple_str() == 'Onion: Vegetable, Healthy, Vitamin C'


class TestIngredient:
    aliment = Aliment(name='onion')

    def test_ingredient_no_quantity_type_creation(self):
        ing = Ingredient(aliment=self.aliment, quantity=5.0)

        assert ing.aliment is self.aliment and ing.quantity == 5.0 and ing.quantity_type == ''

    def test_ingredient_no_optional_creation(self):
        ing = Ingredient(aliment=self.aliment, quantity=10.0, quantity_type='gr')

        assert ing.aliment is self.aliment and ing.quantity == 10.0 and ing.quantity_type == 'gr' and not ing.optional

    def test_ingredient_optional_creation(self):
        ing = Ingredient(aliment=self.aliment, quantity=10.0, quantity_type='gr', optional=True)

        assert ing.aliment is self.aliment and ing.quantity == 10.0 and ing.quantity_type == 'gr' and ing.optional

    def test_ingredient_simple_str(self):
        ing = Ingredient(aliment=self.aliment, quantity=10.0, quantity_type='gr', optional=True)

        assert ing.simple_str() == 'Onion: 10.0 gr (Optional)'

class TestRecipe:
    ingredients = [
        Ingredient(aliment=Aliment(name='onion'), quantity=10.0, quantity_type='gr'),
        Ingredient(aliment=Aliment(name='olive oil'), quantity=2, quantity_type='spoon', optional=True)
    ]

    def test_recipe_no_tags_time_creation(self):
        recipe = Recipe(name='Fried onions', num_people=2, ingredients=self.ingredients,
                        steps=['Chop the onion', 'Fry it!'], category='Main')

        assert recipe.name == 'Fried onions' and recipe.num_people == 2 and recipe.ingredients == self.ingredients and \
               recipe.steps == ['Chop the onion', 'Fry it!'] and recipe.category == 'main' and recipe.tags == [] and \
               recipe.time is None

    def test_recipe_no_time_creation(self):
        recipe = Recipe(name='Fried onions', num_people=2, ingredients=self.ingredients,
                        steps=['Chop the onion', 'Fry it!'], category='Main', tags=['Quick', 'vegan '])

        assert recipe.name == 'Fried onions' and recipe.num_people == 2 and recipe.ingredients == self.ingredients and \
               recipe.steps == ['Chop the onion', 'Fry it!'] and recipe.category == 'main' and \
               recipe.tags == ['quick', 'vegan'] and recipe.time is None

    def test_recipe_creation(self):
        recipe = Recipe(name='Fried onions', num_people=2, ingredients=self.ingredients,
                        steps=['Chop the onion', 'Fry it!'], category='Main', tags=['Quick', 'vegan '], time=20)

        assert recipe.name == 'Fried onions' and recipe.num_people == 2 and recipe.ingredients == self.ingredients and \
               recipe.steps == ['Chop the onion', 'Fry it!'] and recipe.category == 'main' and \
               recipe.tags == ['quick', 'vegan'] and recipe.time == 20

    def test_recipe_whitespaces_creation(self):
        recipe = Recipe(name='Fried   onions   ', num_people=2, ingredients=self.ingredients,
                        steps=[' Chop        the onion', 'Fry it! '], category='Main  ', tags=[' Quick', ' vegan '],
                        time=20)

        assert recipe.name == 'Fried onions' and recipe.num_people == 2 and recipe.ingredients == self.ingredients and \
               recipe.steps == ['Chop the onion', 'Fry it!'] and recipe.category == 'main' and \
               recipe.tags == ['quick', 'vegan'] and recipe.time == 20

    def test_recipe_simple_str(self):
        recipe = Recipe(name='Fried onions', num_people=2, ingredients=self.ingredients,
                        steps=['Chop the onion', 'Fry it!'], category='Main', tags=['Quick', 'vegan '], time=20)

        assert recipe.simple_str() == 'Fried onions (Main): Quick, Vegan'

    def test_recipe_get_non_optional_aliments(self):
        recipe = Recipe(name='Fried onions', num_people=2, ingredients=self.ingredients,
                        steps=['Chop the onion', 'Fry it!'], category='Main', tags=['Quick', 'vegan '], time=20)

        assert recipe.get_not_optional_aliments() == [i.aliment for i in self.ingredients if not i.optional]
