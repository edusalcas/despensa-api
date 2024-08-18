import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {map} from "rxjs/operators";
import {Observable, Subscription} from "rxjs";
import {Recipe} from "../../entities/recipe";
import {AlimentsService} from "../aliments_service/aliments.service";
import {error} from "@angular/compiler-cli/src/transformers/util";
import { NumericLiteral } from 'typescript';

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
    private alimentService: AlimentsService,
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

  insertRecipe(recipe: unknown): Observable<Recipe> {
    if (!(recipe instanceof Recipe)) {
      throw new Error('Invalid argument: recipe must be an instance of Recipe class');
    }

    return this.http.post<Recipe>(this.url, recipe, this.httpOptions).pipe(map(data => {
      return Recipe.cast(data);
    }));
  }

  updateRecipe(recipe: Recipe): Observable<any> {
    return this.http.put(this.url.concat(`/${recipe._db_id}`), recipe, this.httpOptions).pipe(map(data => {
      return data;
    }));
  }

  deleteRecipe(recipe_id: Number): Observable<any> {
    return this.http.delete(this.url.concat(`/${recipe_id}`), this.httpOptions).pipe(map(data => {
      return data;
    }));
  }

}
