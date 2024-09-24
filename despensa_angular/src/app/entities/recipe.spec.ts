import { Recipe } from './recipe';
import { Ingredient } from './ingredient';
import { Food } from './food';

describe('Recipe', () => {
  let recipe: Recipe;
  let ingredients: Ingredient[];

  beforeEach(() => {
    ingredients = [
      new Ingredient(new Food(1, 'Tomatoe', ['Vegetable']), 100, 'gr', false, 1),
      new Ingredient(new Food(2, 'Salt', ['Basic']), 1, 'tsp', false, 2)
    ];

    recipe = new Recipe(
      1,
      'Tomato Soup',
      4,
      ingredients,
      ['Chop tomatoes', 'Boil water', 'Add ingredients', 'Simmer for 20 minutes'],
      'Soup',
      ['Vegetarian', 'Low calorie'],
      30
    );
  });

  it('should create a recipe instance correctly', () => {
    expect(recipe).toBeTruthy();
    expect(recipe._db_id).toBe(1);
    expect(recipe._name).toBe('Tomato Soup');
    expect(recipe._num_people).toBe(4);
    expect(recipe._ingredients).toEqual(ingredients);
    expect(recipe._steps).toEqual([
      'Chop tomatoes',
      'Boil water',
      'Add ingredients',
      'Simmer for 20 minutes'
    ]);
    expect(recipe._category).toBe('Soup');
    expect(recipe._tags).toEqual(['Vegetarian', 'Low calorie']);
    expect(recipe._time).toBe(30);
  });

  it('should update the recipe name', () => {
    recipe._name = 'Spicy Tomato Soup';
    expect(recipe._name).toBe('Spicy Tomato Soup');
  });

  it('should update the number of people', () => {
    recipe._num_people = 6;
    expect(recipe._num_people).toBe(6);
  });

  it('should update ingredients', () => {
    const newIngredients = [  
      new Ingredient(new Food(3, 'Potato', ['Vegetable']), 3, 'pieces', false, 3),
      new Ingredient(new Food(4, 'Pepper', ['Basic']), 1, 'tsp', false, 4)
    ];
    recipe._ingredients = newIngredients;
    expect(recipe._ingredients).toEqual(newIngredients);
  });

  it('should update steps', () => {
    const newSteps = ['Peel potatoes', 'Boil water', 'Add potatoes', 'Simmer for 30 minutes'];
    recipe._steps = newSteps;
    expect(recipe._steps).toEqual(newSteps);
  });

  it('should update category', () => {
    recipe._category = 'Main course';
    expect(recipe._category).toBe('Main course');
  });

  it('should update tags', () => {
    const newTags = ['Gluten free', 'Low sodium'];
    recipe._tags = newTags;
    expect(recipe._tags).toEqual(newTags);
  });

  it('should update time', () => {
    recipe._time = 45;
    expect(recipe._time).toBe(45);
  });

  it('should consider two recipes equal if they have the same db_id and name', () => {
    const recipe2 = new Recipe(1, 'Tomato Soup', 4, ingredients, ['Chop', 'Cook'], 'Soup', ['Vegan'], 20);
    expect(recipe.equals(recipe2)).toBe(true);
  });

  it('should not consider two recipes equal if they have different db_id or name', () => {
    const recipe2 = new Recipe(2, 'Potato Soup', 4, ingredients, ['Peel', 'Cook'], 'Soup', ['Vegan'], 25);
    expect(recipe.equals(recipe2)).toBe(false);
  });

  it('should cast a recipe from raw data', () => {
    const data = {
      db_id: 2,
      name: 'Salad',
      num_people: 2,
      ingredients: [
        {
            aliment: {db_id: 5, name: 'Lettuce', tags: ['Vegetable']},
            quantity: 150,
            quantity_type: 'gr',
            optional: 1,
            db_id: 2
        }
      ],
      steps: ['Wash lettuce', 'Serve'],
      category: 'Appetizer',
      tags: ['Vegan', 'Healthy'],
      time: 10
    };

    const castedRecipe = Recipe.cast(data);

    expect(castedRecipe._db_id).toBe(2);
    expect(castedRecipe._name).toBe('Salad');
    expect(castedRecipe._num_people).toBe(2);
    expect(castedRecipe._ingredients.length).toBe(1);
    expect(castedRecipe._ingredients[0]._aliment._name).toBe('Lettuce');
    expect(castedRecipe._steps).toEqual(['Wash lettuce', 'Serve']);
    expect(castedRecipe._category).toBe('Appetizer');
    expect(castedRecipe._tags).toEqual(['Vegan', 'Healthy']);
    expect(castedRecipe._time).toBe(10);
  });
});
