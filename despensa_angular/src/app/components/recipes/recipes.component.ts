import { Component } from '@angular/core';
import {HeaderComponent} from "../header/header.component";
import {FooterComponent} from "../footer/footer.component";
import {RecipesMainComponent} from "./recipes-main/recipes-main.component";


@Component({
  selector: 'app-recipes',
  templateUrl: 'recipes.component.html',
  standalone: true,
  imports: [
    HeaderComponent,
    FooterComponent,
    RecipesMainComponent
  ],
  styleUrl: 'recipes.component.css'
})
export class RecipesComponent {

  public header = 'Meat Planner App';

  public navBar: { page: string, name: string }[] =
    [{page: "/index", name: "Index"},
      {page: "/aliments", name: "Aliments"},
      {page: "/pantry", name: "Pantry"},
      {page: "/shopping_list", name: "Shopping List"}];
}
