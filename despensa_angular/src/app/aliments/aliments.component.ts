import {Component} from "@angular/core";

@Component({
  selector: "aliments",
  templateUrl: `aliments.component.html`,
  styleUrl: `aliments.component.css`,
})
export class AlimentsComponent {

  public headerContent: string = "Meal Planner App";

  public navBar: [{ page: string, name: string }] = [{page: "/index", name: "Index"}];
}
