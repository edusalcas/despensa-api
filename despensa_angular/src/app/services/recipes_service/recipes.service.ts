import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {map} from "rxjs/operators";
import {Observable} from "rxjs";
import {Recipe} from "../../entities/recipe";
import {IngredientsService} from "../ingredientsService/ingredients.service";

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
    private ingredientsService: IngredientsService,
  ) {
  }

  get(id: number) {
    return this.http.get<any>(this.url.concat(`/${id}`), {headers: {Accept: 'application/json'}})
      .pipe(
        map(data => {
          let {db_id, name, num_people, ingredients, steps, category, tags, time} = data;
          steps = this.castAsStringArr(steps);
          tags = this.castAsStringArr(tags);
          ingredients = this.castAsArrayIngredients(ingredients);
          return new Recipe(db_id,
            name,
            num_people,
            ingredients,
            steps,
            category,
            tags,
            time);
        }));
  }

  getAllRecipes(): Observable<Recipe[]> {
    return this.http.get<any[]>(this.url, {headers: {Accept: 'application/json'}})
      .pipe(map(data => data.map(data => {
        let {db_id, name, num_people, ingredients, steps, category, tags, time} = data;
        steps = this.castAsStringArr(steps);
        tags = this.castAsStringArr(tags);
        ingredients = this.castAsArrayIngredients(ingredients);
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

  private castAsArrayIngredients(ingredients: any[]) {
    return ingredients.map(ingredient => {
      return this.ingredientsService.castAsIngredient(ingredient);
    });
  }

  private castAsStringArr(str: any) {
    if (typeof str !== 'string') str = str.toString();
    return str.split(',').map((tag: { trim: () => any; }) => tag.trim());
  }
}
