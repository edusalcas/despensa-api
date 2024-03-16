import {Component, OnDestroy, OnInit} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {NgSelectModule} from "@ng-select/ng-select";
import {FormBuilder, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {Subscription} from "rxjs";
import {ActivatedRoute} from "@angular/router";

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
export class EditRecipeComponent implements OnInit, OnDestroy {

  protected recipe: Recipe | undefined;
  private subs: Subscription[] = [];
  form: FormGroup;

  constructor(private recipeServ: RecipesService,
              private router: ActivatedRoute,
              private fb: FormBuilder) {
    this.form = this.fb.group({

    });
  }

  ngOnInit() {
    let id = -1;
    this.subs.push(this.router.params.subscribe({
      next: value => {
        id = value["id"];
      }
    }));

    this.subs.push(this.recipeServ.get(id).subscribe({
      next: data => {
        this.recipe = data;
      },
      error: err => {
        console.error(err);
      }
    }));
  }

  ngOnDestroy(): void {
    this.subs.forEach(sub => sub.unsubscribe());
  }

}
