export class Food {

  private db_id: number;

  private name: string;

  private tags: string[];

  constructor(id: number, name: string, tags: string[]) {
    this.db_id = id;
    this.name = name;
    this.tags = tags;
  }

  set _name(name: string) {
    this.name = name;
  }


  get _name(): string {
    return this.name;
  }

  set _db_id(db_id: number) {
    this.db_id = db_id;
  }


  get _db_id(): number {
    return this.db_id;
  }

  set _tags(tags: string[]) {
    this.tags = tags;
  }


  get _tags(): string[] {
    return this.tags;
  }

  equals(other: Food): boolean {
    return this._name === other._name && this._db_id === other._db_id && this.tagsEquals(other._tags);
  }

  private tagsEquals(otherTags: Array<string>) {
    return otherTags && this._tags.length === otherTags.length && this._tags.every((a, index) => a === otherTags[index]);
  }

  hash(): string {
    return `${this._name}${this._db_id}`;
  }
}
