import { Component } from '@angular/core';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrl: './index.component.css'
})
export class IndexComponent {

  public header: string = "Meal Planner App";

  public navBar: { page: string, name: string }[] =
    [{page: "/aliments", name: "Aliments"},
      {page: "/recipes", name: "Recipes"},
      {page: "/pantry", name: "Pantry"},
      {page: "/shopping_list", name: "Shopping List"}];

  public login = true;
}
