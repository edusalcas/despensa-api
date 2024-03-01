export class Food {

  private _db_id: number;

  private _name: string;

  private _tags: string[];

  constructor(id:number, name:string, tags:string[]) {
    this._db_id = id;
    this._name = name;
    this._tags = tags;
  }

  get db_id(): number {
    return this._db_id;
  }

  set db_id(value: number) {
    this._db_id = value;
  }

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    this._name = value;
  }

  get tags(): string[] {
    return this._tags;
  }

  set tags(value: string[]) {
    this._tags = value;
  }
}
