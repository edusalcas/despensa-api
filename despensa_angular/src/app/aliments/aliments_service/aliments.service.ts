import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Food} from "../entities/food";
import {Observable} from "rxjs";

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
      private http:HttpClient,
    ) { }

    getAllFood(){
      return this.http.get<Food[]>(this.url, { headers: { Accept: 'application/json' } });
    }

    insertFood(food:Food):Observable<boolean>{
      return this.http.post<boolean>(this.url, food,  this.httpOptions );
    }
}
