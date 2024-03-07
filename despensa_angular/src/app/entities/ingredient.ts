import {Food} from "./food";

export class Ingredient {

  private aliment: Food;
  private quantity: number;
  private quantity_type: string;
  private optional: boolean;
  private db_id: number ;


  constructor(aliment: Food, quantity: number, quantity_type: string, optional: boolean, db_id: number) {
    this.aliment = aliment;
    this.quantity = quantity;
    this.quantity_type = quantity_type;
    this.optional = optional;
    this.db_id = db_id;
  }


  get _aliment(): Food {
    return this.aliment;
  }

  set _aliment(value: Food) {
    this.aliment = value;
  }

  get _quantity(): number {
    return this.quantity;
  }

  set _quantity(value: number) {
    this.quantity = value;
  }

  get _quantity_type(): string {
    return this.quantity_type;
  }

  set _quantity_type(value: string) {
    this.quantity_type = value;
  }

  get _optional(): boolean {
    return this.optional;
  }

  set _optional(value: boolean) {
    this.optional = value;
  }

  get _db_id(): number {
    return this.db_id;
  }

  set _db_id(value: number) {
    this.db_id = value;
  }

  equals(other: Ingredient) {
    return this._aliment.equals(other._aliment) && this._db_id === other._db_id
  }
}
