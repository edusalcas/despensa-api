import {Component} from "@angular/core";
import {HeaderComponent} from "../header/header.component";
import {FooterComponent} from "../footer/footer.component";
import {AlimentsMainComponent} from "./aliments-main/aliments-main.component";
@Component({
  selector: "aliments",
  templateUrl: `aliments.component.html`,
  styleUrl: `aliments.component.css`,
  imports: [
    HeaderComponent,
    FooterComponent,
    AlimentsMainComponent
  ],
  standalone: true
})
export class AlimentsComponent {

  public headerContent: string = "Meal Planner App";

  public navBar: { page: string, name: string }[] =
    [{page: "/index", name: "Index"},
      {page: "/recipes", name: "Recipes"},
      {page: "/pantry", name: "Pantry"},
      {page: "/shopping_list", name: "Shopping List"}];
}
