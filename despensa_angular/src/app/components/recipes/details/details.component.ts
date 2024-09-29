import {Component, OnDestroy, OnInit, ViewChild, ViewContainerRef} from '@angular/core';
import {HeaderComponent} from "../../header/header.component";
import {FooterComponent} from "../../footer/footer.component";
import {NgClass, NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {ActivatedRoute, RouterLink, Router} from "@angular/router";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes.service";
import {Subscription} from "rxjs";
import {
  NgbAccordionBody,
  NgbAccordionCollapse,
  NgbAccordionDirective,
  NgbAccordionHeader,
  NgbAccordionItem, NgbAccordionToggle, NgbCollapse,
  NgbDropdownAnchor
} from "@ng-bootstrap/ng-bootstrap";

import {EditRecipeComponent} from "../edit-recipe/edit-recipe.component";
import {ModalService} from "../../../services/modal.service";

@Component({
  selector: 'app-details',
  standalone: true,
  imports: [
    HeaderComponent,
    FooterComponent,
    NgOptimizedImage,
    NgForOf,
    NgIf,
    NgbAccordionDirective,
    NgbAccordionHeader,
    NgbAccordionItem,
    NgbDropdownAnchor,
    NgbAccordionCollapse,
    NgbAccordionBody,
    NgbCollapse,
    NgClass,
    NgbAccordionToggle,
    RouterLink,

    EditRecipeComponent,
  ],
  templateUrl: './details.component.html',
  styleUrl: './details.component.css'
})
export class DetailsComponent implements OnInit, OnDestroy{
  protected recipe: Recipe | undefined;
  private subRouter: Subscription | undefined;
  private subRecServ: Subscription | undefined;
  protected isPanelIngOpen: boolean = false;
  protected isPanelStpsOpen: boolean = false;

  @ViewChild('modal', {read: ViewContainerRef})
  private entry!: ViewContainerRef;
  private subs: Subscription[] = [];
  
  constructor(
    private activatedRouter: ActivatedRoute,
    private router: Router,
    private recipeService: RecipesService,  
    private modalService: ModalService,
  ) {}

  ngOnInit() {
    let id = -1;
    this.subRouter = this.activatedRouter.params.subscribe({
      next: value => {
        id = value["id"];
      }
    });

    this.subRecServ = this.recipeService.get(id).subscribe({
      next: data => {
        this.recipe = data;
      },
      error: err => {
        console.error(err);
      }
    });
  }

  ngOnDestroy() {
    this.subRouter?.unsubscribe();
    this.subRecServ?.unsubscribe();
  }

  async showModalEditRecipe() {
    if (this.recipe) {
      this.subs.push(this.modalService.openModal(this.entry, EditRecipeComponent, this.recipe).subscribe({
        next: value => {
          value = Recipe.cast(value);
          if (value instanceof Recipe) {
            let new_recipe = Recipe.cast(value)
            new_recipe._db_id = this.recipe!._db_id
            this.recipe = new_recipe
          }
          this.recipeService.updateRecipe(this.recipe!).subscribe({
            next: value1 => {
              console.log(value1);
            },
            error: err => {
              console.log(err, err.error);
            }
          })
        }
      }));
    }
  }

  async deleteRecipe() {
    if (this.recipe) {
      this.recipeService.deleteRecipe(this.recipe!._db_id).subscribe({
        next: value1 => {
          console.log(value1);
        },
        error: err => {
          console.log(err, err.error);
        }
      });
    }
    this.router.navigate(["/index"]).catch(err => console.error(err));
  }

}
