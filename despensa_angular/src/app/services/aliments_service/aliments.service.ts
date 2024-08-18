import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Food} from "../../entities/food";
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

  getAllFood(): Observable<Food[]> {
    return this.http.get<any[]>(this.url, {headers: {Accept: 'application/json'}})
      .pipe(map(data => data.map(data => {
        return Food.cast(data);
      })))
  }

  insertFood(food: unknown): Observable<Food> {
    if (!(food instanceof Food)) {
      throw new Error('Invalid argument: food must be an instance of Food class');
    }

    return this.http.post<Food>(this.url, food, this.httpOptions).pipe(map(data => {
      return Food.cast(data);
    }));
  }

  updateFood(food: Food): Observable<any> {
    return this.http.put(this.url.concat(`/${food._db_id}`), food, this.httpOptions);
  }

  deleteFood(food_id: Number): Observable<any> {
    return this.http.delete(this.url.concat(`/${food_id}`), this.httpOptions);
  }


}
