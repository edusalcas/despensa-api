import {Component, OnInit, ViewChild} from '@angular/core';
import {AlimentsService} from "../aliments_service/aliments.service";
import {Food} from "../entities/food";
import {NgForm} from "@angular/forms";

@Component({
  selector: 'app-aliments-main',
  templateUrl: './aliments-main.component.html',
  styleUrl: './aliments-main.component.css'
})
export class AlimentsMainComponent implements OnInit {

  @ViewChild('addFoodForm') addFoodForm: NgForm | undefined;
  tags = '';

  foodList: Array<{ aliment: Food, editable: boolean }> = [];

  isModalHidden: boolean = true;

  hasErrors: boolean = false;

  errorMessage: string = 'The food name is already in use';

  get tagsArray() {
    return this.tags.split(',').map(tag => tag.trim());
  }


  constructor(
    private alimentsService: AlimentsService,
  ) {
  }

  ngOnInit() {
    this.retrieveFoodData();
  }

  /**
   * This method toggles the value of the `isModalHidden` variable. Due to two-way data binding,
   * a class is dynamically added to or removed from the modal, thereby changing its visibility.
   * If the modal is hidden, the associated form is reset.
   */
  changeModalState() {
    this.isModalHidden = !this.isModalHidden;

    if (!this.isModalHidden) {
      this.addFoodForm?.reset();
    }
  }

  /**
   * This asynchronous method attempts to insert data into the database. If the insertion is successful,
   * it retrieves the food data from the database and hides the modal. If the insertion is unsuccessful,
   * it sets `hasErrors` to true. Any unhandled errors during the operation are logged to the console.
   */
  async validateForm(data: Food) {
    try {
      const isInsert: boolean = await this.fetchNewFood(data);
      if (isInsert) {
        this.hasErrors = false;
        this.retrieveFoodData();
        this.changeModalState();
      } else {
        this.hasErrors = true;
      }
    } catch (err) {
      console.log(err);
    }
  }

  /**
   * This method returns a new Promise. If the Promise is resolved with a boolean value of true,
   * it indicates a successful insertion. If it is resolved with a boolean value of false,
   * it indicates an unsuccessful insertion. Any errors during the insertion process are propagated
   * by rejecting the Promise.
   * @param food {Food}
   */
  fetchNewFood(food: Food): Promise<boolean> {
    if (food.tags) food.tags = this.tagsArray;
    else food.tags = [""];
    return new Promise((resolve, reject) => {
      this.alimentsService.insertFood(food).subscribe({
          next: data => {
            resolve(data);
          },
          error: error => {
            reject(error);
          }
        }
      );
    });
  }

  retrieveFoodData() {
    this.alimentsService.getAllFood().subscribe(data => {
      data.forEach((food, index) => {
        if (this.foodList[index] && this.foodList[index].aliment !== food) {
          this.foodList[index].aliment = food;
        } else {
          this.foodList.push({aliment: food, editable: false});
        }
      });
    });
  }

  editTags(index: number) {
    this.foodList[index].editable = true;
  }

  saveData(index: number, event: any) {
    const newTags = event.target?.innerText.split(",").map((str: string) => str.trim());
    this.foodList[index].editable = false;
    this.foodList[index].aliment.tags = newTags;
    new Promise((resolve, reject) => {
      this.alimentsService.updateFood(this.foodList[index].aliment).subscribe({
        next: data => {
          resolve(data);
        },
        error: err => {
          reject(err);
        }
      });
    }).then(() => {
      this.retrieveFoodData();
    })
      .catch(err => console.error("An error has occurs", err));
  }
}
