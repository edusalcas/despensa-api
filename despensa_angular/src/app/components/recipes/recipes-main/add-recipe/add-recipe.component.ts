import {AfterViewInit, Component, EventEmitter, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import {FormsModule} from "@angular/forms";
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
    NgSelectModule
  ],
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css'
})
export class AddRecipeComponent implements OnInit, OnDestroy, AfterViewInit {

  protected isEditing: boolean;
  protected ingredientsList: Food[] = [];
  protected subscribeIngredient: Subscription | undefined;
  @Output() close = new EventEmitter<any>();
  @Output() confirm = new EventEmitter<any>();
  @ViewChild('modal')
  modal: any;
  body: string | undefined;

  constructor(private alimentsService: AlimentsService,
              private modalService: NgbModal) {
    this.isEditing = false;
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
        console.log(result);
        this.confirm.emit(result);
      },
      () => {
        this.close.emit();
      }
    );
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

  inputs: { value: string, filteredIngredients: Food[] }[] = [];

  addInput() {
    this.inputs.push({value: '', filteredIngredients: []});
  }

  removeInput(index: number) {
    this.inputs.splice(index, 1);
  }

  search(index: number): void {
    if (this.inputs[index].value) {
      this.inputs[index].filteredIngredients = this.ingredientsList.filter(item =>
        item._name.toLowerCase().includes(this.inputs[index].value.toLowerCase())
      );
    } else {
      this.inputs[index].filteredIngredients = [];
    }
  }
}
