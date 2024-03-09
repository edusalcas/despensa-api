import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {HeaderComponent} from "./components/header/header.component";
import {FooterComponent} from "./components/footer/footer.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  public header = 'Meal Planner App';

  public navBar: { page: string, name: string }[] =
    [{page: "/index", name: "Index"},
      {page: "/aliments", name: "Aliments"},
      {page: "/recipes", name: "Recipes"},
      {page: "/pantry", name: "Pantry"},
      {page: "/shopping_list", name: "Shopping List"}];
}
