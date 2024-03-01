import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Food} from "../entities/food";

@Injectable({
  providedIn: 'root'
})
export class AlimentsService {
  private url: string = "http://localhost:5000/rest/aliments";
  constructor(
    private http:HttpClient,
  ) { }

  getFood(){
    return this.http.get<Food[]>(this.url, { headers: { Accept: 'application/json' } });
  }

  insertFood(db_id: number, name: string, tags: string[]){
    const food = new Food(db_id, name,tags);
    return this.http.post(
      this.url,
      {
        headers: { Accept: 'application/json' },
        body: JSON.stringify(food),
      })
  }
}
