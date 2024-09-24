import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  OnDestroy,
  OnInit,
  Output,
  ViewChild
} from '@angular/core';
import {FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {JsonPipe, NgForOf, NgIf} from "@angular/common";
import {Food} from "../../../entities/food";
import {debounceTime, distinctUntilChanged, merge, Observable, OperatorFunction, Subscription} from "rxjs";
import {AlimentsService} from "../../../services/aliments.service";
import {NgSelectModule} from "@ng-select/ng-select";
import {NgbModal, NgbTypeahead} from "@ng-bootstrap/ng-bootstrap";
import {map} from "rxjs/operators";
import {Recipe} from "../../../entities/recipe";
import {RecipesService} from "../../../services/recipes_service/recipes.service";

@Component({
  selector: 'app-add-recipe',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    NgIf,
    NgSelectModule,
    ReactiveFormsModule,
    NgbTypeahead,
    JsonPipe
  ],
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css'
})
export class AddRecipeComponent implements OnInit, OnDestroy, AfterViewInit {

  protected ingredientsList: Food[] = [];
  protected subs: Subscription[] = [];
  @Output() close = new EventEmitter<any>();
  @Output() confirm = new EventEmitter<any>();
  @ViewChild('modal')
  private modal: any;
  protected form: FormGroup;
  protected units = ["gr", "mL", "L", "units", "pinch"];
  
  constructor(private alimentsService: AlimentsService,
              private recipeService: RecipesService,
              private modalService: NgbModal,
              private cdr: ChangeDetectorRef,
              private fb: FormBuilder) {

    this.form = this.fb.group({
      name: '',
      num_people: '',
      ingredients: this.fb.array([]),
      steps: this.fb.array([]),
      category: '',
      tags: '',
      time: ''
    })
  }

  ngOnInit(): void {
    this.subs.push(this.retrieveIngredients());
  }

  ngOnDestroy(): void {
    this.subs?.forEach(sub => sub.unsubscribe());
  }

  ngAfterViewInit(): void {
    this.open()
  }

  open() {
    this.modalService.open(this.modal, {centered: true, scrollable: true, backdrop: "static"}).result.then(
      result => {
        console.log(result);
        this.confirm.emit(result);
      },
      () => {
        this.close.emit();
      }
    );
  }

  async validateForm(event: any, value: any, form: any) {
    event.preventDefault();
    await this.insertNewIngredients(value.ingredients);
    value = Recipe.cast(value);
    console.log(value);
    if (value instanceof Recipe) {
      value._tags = value._tags.toString().split(',').map((tag: { trim: () => any; }) => tag.trim());
    }
    this.recipeService.insertRecipe(value).subscribe({
      next: value1 => {
        form.close(value1);
      },
      error: err => {
        console.log(err, err.error);
      }
    })
  }

  get ingredients() {
    return this.form.get('ingredients') as FormArray;
  }

  get steps() {
    return this.form.get('steps') as FormArray;
  }

  addIngredient(event?: Event) {
    event?.preventDefault();
    const ingredientGroup = this.fb.group({
      aliment: '',
      quantity: '',
      quantity_type: ''
    });
    this.ingredients.push(ingredientGroup);
  }

  removeIngredient(index: number, event: Event) {
    event.preventDefault();
    this.ingredients.removeAt(index);
  }

  addStep(event: any) {
    event?.preventDefault();
    const stepGroup = this.fb.control('');

    this.steps.push(stepGroup);
  }

  removeStep(index: number, event: Event) {
    event.preventDefault();
    this.steps.removeAt(index);
  }

  retrieveIngredients() {
    return this.alimentsService.getAllFood().subscribe({
      next: data => {
        data.forEach((food: Food, index: number) => {
          const equals = this.ingredientsList[index]?.equals(food);
          if (!this.ingredientsList[index]) {
            this.ingredientsList.push(food);
          } else if (!equals) {
            this.ingredientsList[index] = food;
          }
        });
        this.cdr.detectChanges();
      }
    });
  }

  /**
   * Inserts new ingredients into the ingredients list.
   * If the ingredient is a string, it creates a new Food object and inserts it into the aliments service.
   * After the insertion, it pushes the new ingredient into the ingredients list and triggers change detection.
   * If the ingredient is not a string, it simply resolves the promise.
   *
   * @param {any[]} ingredients - The array of ingredients to be inserted.
   * @returns {Promise} - A promise that resolves when all the ingredients have been processed.
   */
  insertNewIngredients(ingredients: any[]): Promise<any> {
    let promises = ingredients.map(ingredient => {
        return new Promise((resolve) => {
          if (typeof ingredient.aliment === 'string') {
            this.alimentsService.insertFood(new Food(-1, ingredient.aliment, [])).subscribe({
              next: value => {
                ingredient.aliment = value
                this.ingredientsList.push(value);
                this.cdr.detectChanges();
                resolve(value);
              },
              error: err => {
                console.log(err);
                resolve(err);
              }
            })
          } else {
            resolve(true);
          }
        })
      }
    );
    return Promise.all(promises);
  }

  searchIngr: OperatorFunction<string, readonly any[]> = (text$: Observable<string>) => {
    const tratedtext$ = text$.pipe(debounceTime(200), distinctUntilChanged());
    return merge(tratedtext$).pipe(
      map((term) => typeof term === "string" ? this.ingredientsList.filter((v) => v._name.toLowerCase().indexOf(term.toLowerCase()) > -1).slice(0, 10) : []));
  }
  inputFormatIngredient = (result: Food) => result._name;
  resultFormatIngredient = (result: Food) => result._name;
  searchQuantUnit: OperatorFunction<string, readonly any[]> = (text$: Observable<string>) => {
    const tratedtext$ = text$.pipe(debounceTime(200), distinctUntilChanged());

    return merge(tratedtext$).pipe(
      map((term) => this.units.filter((unit) => unit.toLowerCase().includes(<string>term)).slice(0, 10))
    );
  };


}
