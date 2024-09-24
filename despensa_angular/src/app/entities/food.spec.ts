import { Food } from './food';

describe('Food', () => {
  let food: Food;

  beforeEach(() => {
    food = new Food(1, 'Pizza', ['Italian', 'Fast food']);
  });

  it('should create an instance of Food correctly', () => {
    expect(food).toBeTruthy();
    expect(food._db_id).toBe(1);
    expect(food._name).toBe('Pizza');
    expect(food._tags).toEqual(['Italian', 'Fast food']);
  });

  it('should update the name of the food', () => {
    food._name = 'Burger';
    expect(food._name).toBe('Burger');
  });

  it('should update the db_id', () => {
    food._db_id = 2;
    expect(food._db_id).toBe(2);
  });

  it('should update the tags', () => {
    const newTags = ['American', 'Grilled'];
    food._tags = newTags;
    expect(food._tags).toEqual(newTags);
  });

  it('should return true when two foods are equal', () => {
    const sameFood = new Food(1, 'Pizza', ['Italian', 'Fast food']);
    expect(food.equals(sameFood)).toBe(true);
  });

  it('should return false when foods have different db_id', () => {
    const differentFood = new Food(2, 'Pizza', ['Italian', 'Fast food']);
    expect(food.equals(differentFood)).toBe(false);
  });

  it('should return false when foods have different names', () => {
    const differentFood = new Food(1, 'Pasta', ['Italian', 'Fast food']);
    expect(food.equals(differentFood)).toBe(false);
  });

  it('should return false when foods have different tags', () => {
    const differentFood = new Food(1, 'Pizza', ['American', 'Fast food']);
    expect(food.equals(differentFood)).toBe(false);
  });

  it('should generate a correct hash', () => {
    const hash = food.hash();
    expect(hash).toBe('Pizza1');
  });

  it('should cast a valid object to a Food instance', () => {
    const data = {
      db_id: 3,
      name: 'Pasta',
      tags: ['Italian', 'Vegetarian']
    };
    const castedFood = Food.cast(data);
    expect(castedFood._db_id).toBe(3);
    expect(castedFood._name).toBe('Pasta');
    expect(castedFood._tags).toEqual(['Italian', 'Vegetarian']);
  });

  it('should throw an error when trying to cast an invalid object', () => {
    const invalidData = {
      id: 4,  // no 'name' and 'tags' fields
    };
    expect(() => {
      Food.cast(invalidData);
    }).toThrowError('Impossible to cast object to Food');
  });
});
