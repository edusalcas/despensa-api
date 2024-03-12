import { Component } from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {NgSelectModule} from "@ng-select/ng-select";
import {ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-edit-recipe',
  standalone: true,
  imports: [
    NgForOf,
    NgIf,
    NgSelectModule,
    ReactiveFormsModule
  ],
  templateUrl: './edit-recipe.component.html',
  styleUrl: './edit-recipe.component.css'
})
export class EditRecipeComponent {

}
