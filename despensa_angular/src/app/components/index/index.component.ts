import { Component } from '@angular/core';
import {FooterComponent} from "../footer/footer.component";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  standalone: true,
  imports: [
    FooterComponent,
    HeaderComponent
  ],
  styleUrl: './index.component.css'
})
export class IndexComponent {

  protected header: string = "Meal Planner App";

  protected navBar: { page: string, name: string }[] =
    [{page: "/aliments", name: "Aliments"},
      {page: "/recipes", name: "Recipes"},
      {page: "/pantry", name: "Pantry"},
      {page: "/shopping_list", name: "Shopping List"}];

  protected login = true;
}
