import { Ingredient } from './ingredient';
import { Food } from './food';

describe('Ingredient', () => {
  let food: Food;
  let ingredient: Ingredient;

  beforeEach(() => {
    food = new Food(1, 'Apple', ['Fruit']); 
    ingredient = new Ingredient(food, 100, 'gr', false, 1);
  });

  it('should create an instance of Ingredient', () => {
    expect(ingredient).toBeTruthy();
  });

  it('should get and set aliment correctly', () => {
    const newFood = new Food(2, 'Banana', ['Fruit']);
    ingredient._aliment = newFood;
    expect(ingredient._aliment).toBe(newFood);
  });

  it('should get and set quantity correctly', () => {
    ingredient._quantity = 200;
    expect(ingredient._quantity).toBe(200);
  });

  it('should get and set quantity_type correctly', () => {
    ingredient._quantity_type = 'liters';
    expect(ingredient._quantity_type).toBe('liters');
  });

  it('should get and set optional correctly', () => {
    ingredient._optional = true;
    expect(ingredient._optional).toBe(true);
  });

  it('should get and set db_id correctly', () => {
    ingredient._db_id = 2;
    expect(ingredient._db_id).toBe(2);
  });

  it('should return true when two Ingredients are equal', () => {
    const otherIngredient = new Ingredient(food, 100, 'gr', false, 1);
    spyOn(food, 'equals').and.returnValue(true); // Suponiendo que Food tiene un método equals
    expect(ingredient.equals(otherIngredient)).toBeTrue();
  });

  it('should return false when two Ingredients are not equal', () => {
    const otherIngredient = new Ingredient(new Food(2, 'Banana', ['Fruit']), 100, 'gr', false, 1);
    spyOn(food, 'equals').and.returnValue(false);
    expect(ingredient.equals(otherIngredient)).toBeFalse();
  });

  it('should cast an object to Ingredient correctly', () => {
    const rawIngredient = {
      aliment: {db_id: 1, name: 'Apple', tags: ['Fruit']},
      quantity: 150,
      quantity_type: 'gr',
      optional: 1,
      db_id: 2
    };

    const castedIngredient = Ingredient.cast(rawIngredient);

    expect(castedIngredient._aliment).toEqual(food);
    expect(castedIngredient._quantity).toBe(150);
    expect(castedIngredient._quantity_type).toBe('gr');
    expect(castedIngredient._optional).toBe(true); // optional debería ser true porque 1 es truthy
    expect(castedIngredient._db_id).toBe(2);
  });
});
