import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Food} from "../entities/food";
import {map, Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AlimentsService {
  private url: string = "http://localhost:5000/rest/aliments";
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(
    private http: HttpClient,
  ) {
  }

  getAllFood():Observable<Food[]> {
    return this.http.get<Food[]>(this.url, {headers: {Accept: 'application/json'}})
      .pipe(map(data => data.map( data => new Food(data.db_id, data.name, data.tags))))
  }

  insertFood(food: Food):Observable<boolean> {
    return this.http.post<boolean>(this.url, food, this.httpOptions);
  }

  updateFood(food: Food):Observable<any> {
    return this.http.put(this.url.concat(`/${food.db_id}`), food, this.httpOptions);
  }
}
