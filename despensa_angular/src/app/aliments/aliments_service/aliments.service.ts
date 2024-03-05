import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Food} from "../entities/food";
import {catchError, map, Observable, throwError} from "rxjs";
import {throws} from "node:assert";

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

  getAllFood(): Observable<Food[]> {
    return this.http.get<any[]>(this.url, {headers: {Accept: 'application/json'}})
      .pipe(map(data => data.map(data => {
        const {db_id, name, tags} = data;
        return new Food(db_id,
          name,
          tags);
      })))
  }

  insertFood(food: unknown): Observable<boolean> {
    if (!(food instanceof Food)) {
      throw new Error('Invalid argument: food must be an instance of Food class');
    }

    return this.http.post<boolean>(this.url, food, this.httpOptions);
  }

  updateFood(food: Food): Observable<any> {
    return this.http.put(this.url.concat(`/${food._db_id}`), food, this.httpOptions);
  }
}
