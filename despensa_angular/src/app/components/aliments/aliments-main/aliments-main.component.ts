import {Component, OnInit, ViewChild} from '@angular/core';
import {AlimentsService} from "../../../services/aliments_service/aliments.service";
import {FormsModule, NgForm} from "@angular/forms";
import {Food} from "../../../entities/food";
import {NgClass, NgForOf, NgIf} from "@angular/common";

@Component({
  selector: 'app-aliments-main',
  templateUrl: './aliments-main.component.html',
  standalone: true,
  imports: [
    NgForOf,
    NgClass,
    FormsModule,
    NgIf
  ],
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
    return this.tags.split(',').map((tag: { trim: () => any; }) => tag.trim());
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
  async validateForm(data: any) {
    try {
      const {db_id, name, tags} = data;
      const isInsert: boolean = await this.fetchNewFood(new Food(db_id, name, tags));
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

  // @ts-ignore
  // @ts-ignore
  /**
   * This method returns a new Promise. If the Promise is resolved with a boolean value of true,
   * it indicates a successful insertion. If it is resolved with a boolean value of false,
   * it indicates an unsuccessful insertion. Any errors during the insertion process are propagated
   * by rejecting the Promise.
   * @param food {Food}
   */
  fetchNewFood(food: Food): Promise<boolean> {
    food._tags = food._tags ? this.tagsArray : food._tags = [""];
    // @ts-ignore
    return new Promise((resolve: (arg0: any) => void, reject: (arg0: any) => void) => {
      this.alimentsService.insertFood(food).subscribe({
          next: (data: any) => {
            resolve(data);
          },
          error: (error: any) => {
            reject(error);
          }
        }
      );
    });
  }

  retrieveFoodData() {
    this.alimentsService.getAllFood().subscribe({
      next: (data: { forEach: (arg0: (food: Food, index: number) => void) => void; })=> {
        data.forEach((food: Food, index: number) => {
          const equals = this.foodList[index]?.aliment.equals(food);
          if (!this.foodList[index]) {
            this.foodList.push({aliment: food, editable: false});
          } else if (!equals) {
            this.foodList[index].aliment = food;
          }
        });
      },
      error: err => {
        console.error("Error occurred while fetching food data:", err);
      }
    });
  }

  editTags(index: number) {
    this.foodList[index].editable = true;
  }

  saveData(index: number, event: any) {
    const newTags = event.target?.innerText.split(",").map((str: string) => str.trim()).filter((a: string) => a !== "");
    this.foodList[index].editable = false;
    const someChanges = newTags ? this.foodList[index].aliment._tags.some((a, index) => a !== newTags[index]) : false;
    const lenChange = newTags ? newTags.length !== this.foodList[index].aliment._tags.length : false;
    if ((someChanges || lenChange)) {
      this.foodList[index].aliment._tags = newTags;
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
    } else {
      event.target.innerText = newTags.toString();
    }
  }
}
