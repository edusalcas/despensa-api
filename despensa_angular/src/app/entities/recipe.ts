import {Ingredient} from "./ingredient";

export class Recipe {

  private db_id:number;

  private name:string;

  private num_people:number;

  private ingredients:Ingredient[];

  private steps:string[];

  private category:string;

  private tags:string[];

  private time:number;

  constructor(db_id: number, name: string, num_people: number, ingredients:Ingredient[], steps: string[], category: string, tags: string[], time: number) {
    this.db_id = db_id;
    this.name = name;
    this.num_people = num_people;
    this.ingredients = ingredients;
    this.steps = steps;
    this.category = category;
    this.tags = tags;
    this.time = time;
  }


  get _db_id(): number {
    return this.db_id;
  }

  set _db_id(value: number) {
    this.db_id = value;
  }

  get _name(): string {
    return this.name;
  }

  set _name(value: string) {
    this.name = value;
  }

  get _num_people(): number {
    return this.num_people;
  }

  get _ingredients(): Ingredient[] {
    return this.ingredients;
  }

  set _ingredients(value: Ingredient[]) {
    this.ingredients = value;
  }

  set _num_people(value: number) {
    this.num_people = value;
  }

  get _steps(): string[] {
    return this.steps;
  }

  set _steps(value: string[]) {
    this.steps = value;
  }

  get _category(): string {
    return this.category;
  }

  set _category(value: string) {
    this.category = value;
  }

  get _tags(): string[] {
    return this.tags;
  }

  set _tags(value: string[]) {
    this.tags = value;
  }

  get _time(): number {
    return this.time;
  }

  set _time(value: number) {
    this.time = value;
  }

  equals(recipe: Recipe) {
    return this._db_id === recipe._db_id && this._name === recipe._name;
  }

  static cast(data: { db_id: any; name: any; num_people: any; ingredients: any; steps: any; category: any; tags: any; time: any; }) {
    let {db_id, name, num_people, ingredients, steps, category, tags, time} = data;
    db_id = db_id? db_id : 0;
    time = time? time.toString().concat("mins") : "0mins";
    ingredients = this.castAsArrayIngredients(ingredients);
    return new Recipe(db_id,
      name,
      num_people,
      ingredients,
      steps,
      category,
      tags,
      time);
  }

  private static castAsArrayIngredients(ingredients: any[]) {
    return ingredients.map(ingredient => {
      return Ingredient.cast(ingredient);
    });
  }
}
