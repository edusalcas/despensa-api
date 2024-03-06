import {Component, OnInit} from '@angular/core';
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {NgForOf, NgOptimizedImage} from "@angular/common";



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
    NgOptimizedImage
  ],
  styleUrl: './recipes-main.component.css'
})
export class RecipesMainComponent implements OnInit {

  protected recipeList: Recipe[] = [];
  protected filterList: string[] =
    ["Type", "Difficulty", "Num of guests", "Category", "Duration", "Properties", "Nutrition", "Destined for",
      "Cocking", "Season", "Country", "Region", "Spiciness level", "Cost", "Drink"];

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
}
