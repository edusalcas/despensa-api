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
import {debounceTime, distinctUntilChanged, merge, Observable, OperatorFunction, Subscription} from "rxjs";
import {NgSelectModule} from "@ng-select/ng-select";
import {NgbModal, NgbTypeahead} from "@ng-bootstrap/ng-bootstrap";
import {map} from "rxjs/operators";
import {Food} from "../../../entities/food";
import {Recipe} from "../../../entities/recipe";
import {AlimentsService} from "../../../services/aliments.service";
import {RecipesService} from "../../../services/recipes.service";
import { LogService } from '../../../services/log.service';

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
  styleUrl: './add-recipe.component.css',
  providers: [LogService]  // Añadir el servicio aquí
})
export class AddRecipeComponent implements OnInit, OnDestroy, AfterViewInit {

  protected foodList: Food[] = [];
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
              private fb: FormBuilder,
              private logger: LogService) {

    this.form = this.fb.group({
      name: '',
      num_people: '',
      ingredients: this.fb.array([]),
      steps: this.fb.array([]),
      category: '',
      tags: '',
      time: ''
    });
  }

  getFoodList(): Food[] {
    return [...this.foodList];
  }

  getForm(): FormGroup {
    return this.form;
  }

  setForm(recipeData: any): void {
    this.form.setValue({
      name: recipeData.name,
      num_people: recipeData.num_people,
      foods: [],  // Inicializa el FormArray vacío
      steps: [],
      category: recipeData.category,
      tags: recipeData.tags,
      time: recipeData.time
    });
  }

  private log(msg: string): void {
    this.logger.log("[AddRecipeComponent] " + msg);
  }

  ngOnInit(): void {
    this.log("[ngOnInit]");
    this.subs.push(this.retrieveFoods());
    this.log("[ngOnInit] Nº Foods = " + this.foodList.length.toString());
  }

  ngOnDestroy(): void {
    this.log("[ngOnDestroy]");
    this.subs?.forEach(sub => sub.unsubscribe());
  }

  retrieveFoods() {
    this.log('[retrieveFoods]')
    return this.alimentsService.getAllFood().subscribe({
      next: data => {
        data.forEach((food: Food, index: number) => {
          const equals = this.foodList[index]?.equals(food);
          if (!this.foodList[index]) {
            this.foodList.push(food);
          } else if (!equals) {
            this.foodList[index] = food;
          }
        });
        this.cdr.detectChanges();
      }
    });
  }

  ngAfterViewInit(): void {
    this.open()
  }

  open() {
    this.modalService.open(this.modal, {centered: true, scrollable: true, backdrop: "static"}).result.then(
      result => {
        this.confirm.emit(result);
      },
      () => {
        this.close.emit();
      }
    );
  }

  async validateForm(event: any, value: any, form: any) {
    this.log('[validateForm]' + JSON.stringify(value))
    event.preventDefault();
    const newIngredients = await this.updateIngredientsWithFoodObject(value.ingredients);
    value.ingredients = newIngredients
    this.log('[validateForm]' + JSON.stringify(value))
    value = Recipe.cast(value);
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

  addStep(event?: any) {
    event?.preventDefault();
    const stepGroup = this.fb.control('');

    this.steps.push(stepGroup);
  }

  removeStep(index: number, event: Event) {
    event.preventDefault();
    this.steps.removeAt(index);
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
  updateIngredientsWithFoodObject(ingredients: any[]): Promise<any> {
    let promises = ingredients.map(ingredient => {
      this.log(`[updateIngredientsWithFoodObject] Ingredient antes: ${JSON.stringify(ingredient)}`);
  
      return new Promise((resolve) => {
        if (typeof ingredient.aliment === 'string') {
          const existingFood = this.foodList.find(food => food._name.toLowerCase() === ingredient.aliment.toLowerCase());
  
          if (existingFood) {
            this.log(`[updateIngredientsWithFoodObject] El alimento ya existe en foodList: ${JSON.stringify(existingFood)}`);
            ingredient.aliment = existingFood;
            resolve(ingredient);
          } else {
            // Si no existe, lo insertamos en la base de datos
            this.alimentsService.insertFood(new Food(-1, ingredient.aliment, [])).subscribe({
              next: value => {
                this.log(`[updateIngredientsWithFoodObject] Insertado en la BD: ${JSON.stringify(value)}`);
                ingredient.aliment = value;
                // Añadimos el nuevo alimento a foodList
                this.foodList.push(value);
                this.cdr.detectChanges();
                resolve(ingredient);
              },
              error: err => {
                console.log(err);
                resolve(err);
              }
            });
          }
        } else {
          // Si el ingrediente ya es un objeto (no un string), simplemente resolvemos la promesa
          resolve(ingredient);
        }
      });
    });
  
    // Esperamos a que todas las promesas se resuelvan y las devolvemos
    return Promise.all(promises);
  }
  

  searchIngr: OperatorFunction<string, readonly any[]> = (text$: Observable<string>) => {
    const tratedtext$ = text$.pipe(debounceTime(200), distinctUntilChanged());
    return merge(tratedtext$).pipe(
      map((term) => typeof term === "string" ? this.foodList.filter((v) => v._name.toLowerCase().indexOf(term.toLowerCase()) > -1).slice(0, 10) : []));
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
