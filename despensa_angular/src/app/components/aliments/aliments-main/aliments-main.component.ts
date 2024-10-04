import {Component, OnDestroy, OnInit, ViewChild, ViewContainerRef} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {Subscription} from "rxjs";
import {Food} from "../../../entities/food";
import {AlimentsService} from "../../../services/aliments.service";
import {ModalService} from "../../../services/modal.service";
import {AddAlimentComponent} from "../add-aliment/add-aliment.component";

@Component({
  selector: 'app-aliments',
  templateUrl: './aliments-main.component.html',
  styleUrl: "aliments-main.component.css",
  standalone: true,
  imports: [
    NgForOf,
    NgClass,
    FormsModule,
    NgIf,
    NgbModule,
  ]
})
export class AlimentsMainComponent implements OnInit, OnDestroy {

  @ViewChild('modal', {read: ViewContainerRef})
  private modal: any;
  protected foodList: Array<{ aliment: Food, editable: boolean }> = [];
  private subFood: Subscription[] = [];


  constructor(
    private alimentsService: AlimentsService,
    private modalService: ModalService
  ) {
  }

  ngOnInit() {
    this.subFood.push(this.retrieveFoodData());
  }

  ngOnDestroy() {
    this.subFood.forEach(sub => sub.unsubscribe());
  }

  /**
   * Retrieves food data from the service.
   *
   * This function is responsible for retrieving the food data from the alimentsService.
   * It subscribes to the alimentsService's getAllFood method, which returns an Observable.
   * The Observable emits the food data or an error.
   * If the food data is emitted, it iterates over the data and checks if the food item already exists in the food list.
   * If the food item does not exist in the food list, it adds the food item to the list.
   * If the food item exists in the food list and is not equal to the emitted food item, it updates the food item in the list.
   * After iterating over the data, it sorts the food list by the database id of the food items.
   * If an error is emitted, it logs the error.
   *
   * @returns {Subscription} A subscription to the Observable returned by the getAllFood method.
   * @throws Will log an error if the getAllFood method fails.
   */
  retrieveFoodData(): Subscription {
    return this.alimentsService.getAllFood().subscribe({
      next: data => {
        console.log(data)
        data.forEach((food: Food, index: number) => {
          console.log(food, index)
          console.log(this.foodList)
          const equals = this.foodList[index]?.aliment.equals(food);
          if (!this.foodList[index]) {
            this.foodList.push({aliment: food, editable: false});
          } else if (!equals) {
            this.foodList[index].aliment = food;
          }
        });

        this.foodList.sort((a, b) => a.aliment._db_id - b.aliment._db_id)

      },
      error: err => {
        console.error("Error occurred while fetching food data:", err);
      }
    });
  }

  editTags(indexDb: number) {
    const index = this.foodList.findIndex(food => food.aliment._db_id === indexDb);
    this.foodList[index].editable = true;
  }

  getNewTags(event: any): string[] {
    return event.target?.innerText.split(",").map((str: string) => str.trim()).filter((a: string) => a !== "");
  }

  hasChanges(newTags: string[], index: number): boolean {
    const someChanges = newTags ? this.foodList[index].aliment._tags.some((a, index) => a !== newTags[index]) : false;
    const lenChange = newTags ? newTags.length !== this.foodList[index].aliment._tags.length : false;
    return someChanges || lenChange;
  }

  updateFoodTags(newTags: string[], index: number): void {
    this.foodList[index].aliment._tags = newTags;
  }

  updateFoodData(index: number): Promise<any> {
    return new Promise((resolve, reject) => {
      this.subFood.push(this.alimentsService.updateFood(this.foodList[index].aliment).subscribe({
        next: data => {
          resolve(data);
        },
        error: err => {
          reject(err);
        }
      }));
    });
  }

  async deleteFood(food_id: number) {
    //TODO: Check if aliment is in any recipe before delete it
    this.alimentsService.deleteFood(food_id).subscribe({
      next: value1 => {
        console.log(value1);
      },
      error: err => {
        console.log(err, err.error);
      }
    });
    console.log(food_id)
    for (var i = 0; i < this.foodList.length; i++) {
      console.log(this.foodList[i])
      if (this.foodList[i].aliment._db_id == food_id) {
        const deleted = this.foodList.splice(i, i);
        console.log(deleted);
        console.log(this.foodList);
        break;
      }
    }
  }

  /**
   * Asynchronously saves data.
   *
   * This function is responsible for saving the data of a food item in the food list.
   * It first finds the index of the food item in the food list using the provided database id.
   * Then, it gets the new tags from the event and sets the editable property of the food item to false.
   * If there are any changes in the tags, it updates the tags of the food item and updates the food data in the database.
   * If there are no changes, it sets the inner text of the event target to the new tags.
   *
   * @async
   * @param {number} indexDb - The database id of the food item.
   * @param {any} event - The event containing the new tags.
   * @throws Will throw an error if the updateFoodData function fails.
   */
  async saveData(indexDb: number, event: any) {
    // Find the index of the food item in the food list using the database id
    const index = this.foodList.findIndex(food => food.aliment._db_id === indexDb);

    // Get the new tags from the event
    const newTags = this.getNewTags(event);

    // Set the editable property of the food item to false
    this.foodList[index].editable = false;

    // If there are any changes in the tags
    if (this.hasChanges(newTags, index)) {
      // Update the tags of the food item
      this.updateFoodTags(newTags, index);

      try {
        // Update the food data in the database
        await this.updateFoodData(index)
      } catch (err) {
        // Log the error and retrieve the food data
        console.error(err);
        this.subFood.push(this.retrieveFoodData());
      }
    } else {
      // If there are no changes, set the inner text of the event target to the new tags
      event.target.innerText = newTags.toString();
    }
  }

  /**
   * Opens a modal for adding a new food item.
   *
   * This function is responsible for opening a modal that allows the user to add a new food item.
   * It subscribes to the modalService's openModal method, which opens the modal and returns an Observable.
   * The Observable emits the value of the new food item when the modal is closed.
   * If the value is an instance of the Food class, it is added to the food list.
   * If the value is not an instance of the Food class, it tries to cast the value to a Food instance and add it to the food list.
   * If the casting fails, it logs the error.
   *
   * @throws Will log an error if the casting of the value to a Food instance fails.
   */
  openModal() {
    this.subFood.push(this.modalService.openModal(this.modal, AddAlimentComponent).subscribe({
      next: async value => {
        if (value instanceof Food) {
          this.foodList.push({aliment: value, editable: false});
        } else {
          try {
            value = Food.cast(value);
            if (value instanceof Food) this.foodList.push({aliment: value, editable: false});
          } catch (err) {
            console.log(err)
          }
        }
      }
    }));
  }

  public getFoodList() {
    return this.foodList;
  }
}
