import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {Food} from "../../entities/food";
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

  getAllRecipes(): Observable<Recipe[]> {
    return this.http.get<any[]>(this.url, {headers: {Accept: 'application/json'}})
      .pipe(map(data => data.map(data => {
        const {db_id, name, num_people, ingredients, steps, category, tags, time} = data;
        return new Recipe(db_id,
          name,
          num_people,
          ingredients,
          steps,
          category,
          tags,
          time);
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
