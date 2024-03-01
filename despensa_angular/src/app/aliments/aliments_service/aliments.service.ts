import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AlimentsService {
  private url: string = "http://localhost:5000/rest/aliments";
  constructor(private http:HttpClient) { }

  getFood():Observable<unknown>{
    return this.http.get(this.url, { headers: { Accept: 'application/json' } });
  }

  insertFood(name: string, tags: string[], db_id: bigint){
    return this.http.post(this.url, { headers: })
  }
}
