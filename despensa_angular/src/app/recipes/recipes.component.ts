import { Component } from '@angular/core';


@Component({
  selector: 'app-recipes',
  templateUrl: './recipes.component.html',
  styleUrl: './recipes.component.css'
})
export class RecipesComponent {

  public header = 'Meat Planner App';

  public navBar: { page: string, name: string }[] =
    [{page: "/index", name: "Index"},
      {page: "/aliments", name: "Aliments"},
      {page: "/pantry", name: "Pantry"},
      {page: "/shopping_list", name: "Shopping List"}];
}
