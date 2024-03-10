import {AfterViewInit, Component, EventEmitter, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import {FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import {Food} from "../../../../entities/food";
import {Subscription} from "rxjs";
import {AlimentsService} from "../../../../services/aliments_service/aliments.service";
import {NgSelectModule} from "@ng-select/ng-select";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {Recipe} from "../../../../entities/recipe";


@Component({
  selector: 'app-add-recipe',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    NgIf,
    NgSelectModule,
    ReactiveFormsModule
  ],
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css'
})
export class AddRecipeComponent implements OnInit, OnDestroy, AfterViewInit {

  protected isEditing: boolean;
  protected ingredientsList: Food[] = [];
  protected subscribeIngredient!: Subscription;
  @Output() close = new EventEmitter<any>();
  @Output() confirm = new EventEmitter<any>();
  @ViewChild('modal')
  private modal: any;
  protected form: FormGroup;
  protected units = ["gr", "mL", "L"];


  constructor(private alimentsService: AlimentsService,
              private modalService: NgbModal,
              private fb: FormBuilder) {
    this.isEditing = false;
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
    this.subscribeIngredient = this.retriveIngredients();
  }

  ngOnDestroy(): void {
    this.subscribeIngredient?.unsubscribe();
  }

  ngAfterViewInit(): void {
    this.open()
  }

  open() {
    this.modalService.open(this.modal, {centered: true, scrollable: true}).result.then(
      result => {
        try {
          result.ingredients.forEach((ingredient: { aliment: { name: string; db_id: string; }; }) => {
            const db_id = this.ingredientsList.findIndex(food => food._name === ingredient.aliment.name);
            ingredient.aliment.db_id = db_id.toString();
          })

          console.log(result)

          result = Recipe.cast(result)
        } catch (err) {
          console.error(err);
        }
        this.confirm.emit(result);
      },
      () => {
        this.close.emit();
      }
    );
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
      aliment: this.fb.group({
        db_id: '',
        name: '',
        tags: ''
      }),
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

  retriveIngredients() {
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
      }
    });
  }
}
