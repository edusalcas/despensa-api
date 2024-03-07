import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {
  NgbAccordionModule,
  NgbModal,
  NgbModalRef
} from "@ng-bootstrap/ng-bootstrap";
import {FormsModule, NgForm, ReactiveFormsModule} from "@angular/forms";
import {Ingredient} from "../../../entities/ingredient";
import {IngredientsService} from "../../../services/ingredientsService/ingredients.service";
import {AlimentsService} from "../../../services/aliments_service/aliments.service";
import {Food} from "../../../entities/food";


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
    NgbAccordionModule,
    FormsModule,
    NgIf,
    ReactiveFormsModule,
  ],
  styleUrl: './recipes-main.component.css'
})
export class RecipesMainComponent implements OnInit {

  @ViewChild('addEditRecipeForm') addEditRecipeForm: NgForm | undefined;

  protected recipeList: Recipe[] = [];
  protected filterList: { name: string, options: string[] }[] =
    [{name: "Type", options: ["Rica", "Guy"]}, {name: "Difficulty", options: [""]}, {
      name: "Num of guests",
      options: [""]
    },
      {name: "Category", options: [""]}, {name: "Duration", options: [""]}, {name: "Properties", options: [""]},
      {name: "Nutrition", options: [""]}, {name: "Destined for", options: [""]}, {name: "Cocking", options: [""]},
      {name: "Season", options: [""]}, {name: "Country", options: [""]}, {name: "Region", options: [""]},
      {name: "Spiciness level", options: [""]}, {name: "Cost", options: [""]}, {name: "Drink", options: [""]}];

  protected ingredientsList: Food[] = [];

  protected modalRef: NgbModalRef | undefined;

  protected isEditing:boolean;

  constructor(private recipeService: RecipesService,
              private alimentsService: AlimentsService,
              private modalService: NgbModal) {
    this.isEditing = false;
  }

  ngOnInit() {
    this.retriveRecipesFromData();
    this.retriveIngredients();
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

  private retriveIngredients() {
    this.alimentsService.getAllFood().subscribe({
       next: data => {
        data.forEach((food: Food, index: number) => {
          const equals = this.ingredientsList[index]?.equals(food);
          if (!this.ingredientsList[index]) {
            this.ingredientsList.push(food);
          } else if (!equals) {
            this.ingredientsList[index] = food;
          }
        });
      }
    });
  }

  showModalAddRecipe(modal: TemplateRef<any>) {
    this.modalRef = this.modalService.open(modal, {centered: true})
  }

  closeModal() {
    this.modalRef?.close();
  }

  validateForm(value: any) {

  }


}
