import {Component, OnDestroy, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {
  NgbAccordionModule,
  NgbModal,
  NgbModalRef
} from "@ng-bootstrap/ng-bootstrap";
import {FormsModule, NgForm, ReactiveFormsModule} from "@angular/forms";
import {Router} from "@angular/router";
import {Subscription} from "rxjs";
import {AddRecipeComponent} from "./add-recipe/add-recipe.component";


/**
 * - Página de recetas:
 *    - Listado de recetas Done
 *    - Botón añadir receta nueva Done
 *    - Click en receta te lleva a página de receta Done
 * - Página de detalle receta:
 *    - Detalles de la receta, pasos, descripción, ingredientes... Done
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
    AddRecipeComponent,
  ],
  styleUrl: './recipes-main.component.css'
})
export class RecipesMainComponent implements OnInit, OnDestroy {

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



  protected modalRef: NgbModalRef | undefined;
  protected subscribeRecipe: Subscription | undefined;


  constructor(private recipeService: RecipesService,
              private modalService: NgbModal,
              private router: Router
  ) {

  }

  ngOnInit() {
    this.subscribeRecipe = this.retriveRecipesFromData();
  }

  ngOnDestroy() {
    this.subscribeRecipe?.unsubscribe();
  }

  retriveRecipesFromData() {
    return this.recipeService.getAllRecipes().subscribe({
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

  showDetails(indexDb: number) {
    this.router.navigate(["/recipes/details", indexDb]).catch(err => console.error(err));
  }


  showModalAddRecipe(modal: AddRecipeComponent) {
    this.modalRef = this.modalService.open(modal, {centered: true, scrollable: true});
  }

}
