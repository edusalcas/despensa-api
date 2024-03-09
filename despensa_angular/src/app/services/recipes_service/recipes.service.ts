import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {map} from "rxjs/operators";
import {Observable} from "rxjs";
import {Recipe} from "../../entities/recipe";

@Injectable({
  providedIn: 'root'
})
export class RecipesService {
  private url: string = "http://localhost:5000/rest/recipes";
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(
    private http: HttpClient,
  ) {
  }

  get(id: number) {
    return this.http.get<any>(this.url.concat(`/${id}`), {headers: {Accept: 'application/json'}})
      .pipe(
        map(data => {
          return Recipe.cast(data);
        }));
  }



  getAllRecipes(): Observable<Recipe[]> {
    return this.http.get<any[]>(this.url, {headers: {Accept: 'application/json'}})
      .pipe(map(data => data.map(data => {
        return Recipe.cast(data);
      })));
  }

  insertRecipe(recipe: unknown): Observable<boolean> {
    if (!(recipe instanceof Recipe)) {
      throw new Error('Invalid argument: recipe must be an instance of Recipe class');
    }
    return this.http.post<boolean>(this.url, recipe, this.httpOptions);
  }

  updateRecipe(recipe: Recipe): Observable<any> {
    return this.http.put(this.url.concat(`/${recipe._db_id}`), recipe, this.httpOptions);
  }

}
