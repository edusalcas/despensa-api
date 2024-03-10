import {Component, OnDestroy, OnInit, ViewChild, ViewContainerRef} from '@angular/core';
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {
  NgbAccordionModule,
} from "@ng-bootstrap/ng-bootstrap";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Router} from "@angular/router";
import {Subscription} from "rxjs";
import {AddRecipeComponent} from "./add-recipe/add-recipe.component";
import {AddRecipeService} from "../../../services/modal-service/add-recipe.service";


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

  protected recipeList: Recipe[] | undefined;
  protected filterList: { name: string, options: string[] }[] =
    [{name: "Type", options: ["Rica", "Guy"]}, {name: "Difficulty", options: [""]}, {
      name: "Num of guests",
      options: [""]
    },
      {name: "Category", options: [""]}, {name: "Duration", options: [""]}, {name: "Properties", options: [""]},
      {name: "Nutrition", options: [""]}, {name: "Destined for", options: [""]}, {name: "Cocking", options: [""]},
      {name: "Season", options: [""]}, {name: "Country", options: [""]}, {name: "Region", options: [""]},
      {name: "Spiciness level", options: [""]}, {name: "Cost", options: [""]}, {name: "Drink", options: [""]}];

  @ViewChild('modal', {read: ViewContainerRef})
  private entry!: ViewContainerRef;
  private subs: Subscription[] = [];

  constructor(private recipeService: RecipesService,
              private modalService: AddRecipeService,
              private router: Router
  ) {

  }

  ngOnInit() {
    this.subs.push(this.retriveRecipesFromData());
  }

  ngOnDestroy() {
    this.subs?.forEach(sub => sub.unsubscribe());
  }

  retriveRecipesFromData() {
    return this.recipeService.getAllRecipes().subscribe({
      next: data => {
        data.forEach((recipe: Recipe, index: number) => {
          if (this.recipeList) {
            const equals = this.recipeList[index]?.equals(recipe);
            if (!this.recipeList[index]) {
              this.recipeList.push(recipe);
            } else if (!equals) {
              this.recipeList[index] = recipe;
            }
          } else {
            this.recipeList = [];
            this.recipeList.push(recipe);
          }
        });
      }
    })
  }

  showDetails(indexDb: number) {
    this.router.navigate(["/recipes/details", indexDb]).catch(err => console.error(err));
  }


  showModalAddRecipe() {
    this.subs.push(this.modalService.openModal(this.entry).subscribe(
      async value => {
        await this.recipeService.insertRecipe(value).then(resp => resp.subscribe({
          next: () => {

          },
          error: (error: any) => {
            console.error(error);
          }

        })).then(r => {
          if (r) this.subs.push(this.retriveRecipesFromData())
        }).catch(error => console.error(error));
      })
    )
  }

}
