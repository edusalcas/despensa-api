import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import {Food} from "../../../../entities/food";
import {Subscription} from "rxjs";
import {AlimentsService} from "../../../../services/aliments_service/aliments.service";

@Component({
  selector: 'app-add-recipe',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    NgIf
  ],
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css'
})
export class AddRecipeComponent implements OnInit, OnDestroy {

  protected isEditing: any;
  protected ingredientsList: Food[] = [];
  protected subscribeIngredient: Subscription | undefined;

  constructor(private alimentsService: AlimentsService,) {
    this
      .isEditing = false;
  }

  ngOnInit(): void {
    this.subscribeIngredient = this.retriveIngredients();
  }

  ngOnDestroy(): void {
    this.subscribeIngredient?.unsubscribe();
  }


  closeModal() {
    //this.modalRef?.close();
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
  validateForm(value: any) {
    console.log(value)
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
