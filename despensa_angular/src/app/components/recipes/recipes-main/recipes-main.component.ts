import {Component, OnInit} from '@angular/core';
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {NgbDropdown, NgbDropdownMenu, NgbDropdownToggle} from "@ng-bootstrap/ng-bootstrap";


/**
 * - Página de recetas:
 *    - Listado de recetas
 *    - Botón añadir receta nueva
 *    - Click en receta te lleva a página de receta
 * - Página de detalle receta:
 *    - Detalles de la receta, pasos, descripción, ingredientes...
 *    - Botón editar receta te lleva a página edición de receta
 *    - Botón borrar receta
 * - Página de edición de receta:
 *    - Campos para editar/crear una receta
 *    - Botón de guardar receta
 *    - Si [crear receta] campos vacíos
 *    - Si [editar receta] campos correspondientes rellenados
 */
@Component({
  selector: 'app-recipes-main',
  templateUrl: './recipes-main.component.html',
  standalone: true,
  imports: [
    NgForOf,
    NgOptimizedImage,
    NgbDropdown,
    NgbDropdownMenu,
    NgbDropdownToggle,
  ],
  styleUrl: './recipes-main.component.css'
})
export class RecipesMainComponent implements OnInit {

  protected recipeList: Recipe[] = [];
  protected filterList: { name: string, options: string[] }[] =
    [{name: "Type", options: ["Rica","Guy"]}, {name: "Difficulty", options: [""]}, {name: "Num of guests", options: [""]},
      {name: "Category", options: [""]}, {name: "Duration", options: [""]}, {name: "Properties", options: [""]},
      {name: "Nutrition", options: [""]}, {name: "Destined for", options: [""]}, {name: "Cocking", options: [""]},
      {name: "Season", options: [""]}, {name: "Country", options: [""]}, {name: "Region", options: [""]},
      {name: "Spiciness level", options: [""]}, {name: "Cost", options: [""]}, {name: "Drink", options: [""]}];

  constructor(private recipeService: RecipesService) {
  }

  ngOnInit() {
    this.retriveRecipesFromData();
  }

  private retriveRecipesFromData() {
    this.recipeService.getAllRecipes().subscribe({
      next: data => {
        data.forEach((recipe: Recipe, index: number) => {
          const equals = this.recipeList[index]?.equals(recipe);
          if (!this.recipeList[index]) {
            this.recipeList.push(recipe);
          } else if (!equals) {
            this.recipeList[index] = recipe;
          }
        });
      }
    })
  }

  showDetails() {

  }

  showModalAddRecipe() {

  }
}
