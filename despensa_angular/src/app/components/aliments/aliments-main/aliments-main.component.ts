import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {AlimentsService} from "../../../services/aliments_service/aliments.service";
import {FormsModule, NgForm} from "@angular/forms";
import {Food} from "../../../entities/food";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {NgbModal, NgbModalRef, NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-aliments-main',
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

  @ViewChild('addFoodForm') addFoodForm: NgForm | undefined;
  protected tags = '';

  protected foodList: Array<{ aliment: Food, editable: boolean }> = [];

  protected modalReference: NgbModalRef | undefined;

  protected hasErrors: boolean = false;

  protected errorMessage: string | undefined;

  private subFood: Subscription[] = [];

  get tagsArray() {
    return this.tags.split(',').map((tag: { trim: () => any; }) => tag.trim());
  }


  constructor(
    private alimentsService: AlimentsService,
    private modalService: NgbModal
  ) {
  }

  ngOnInit() {
    this.subFood.push(this.retrieveFoodData());
  }

  ngOnDestroy() {
    this.subFood.forEach(sub => sub.unsubscribe());
  }

  /**
   * This method toggles the value of the `isModalHidden` variable. Due to two-way data binding,
   * a class is dynamically added to or removed from the modal, thereby changing its visibility.
   * If the modal is hidden, the associated form is reset.
   */
  openModal(modal: any) {
    this.modalReference = this.modalService.open(modal, {centered: true});
  }

  closeModal() {
    this.modalReference?.close();
  }

  /**
   * This asynchronous method attempts to insert data into the database. If the insertion is successful,
   * it retrieves the food data from the database and hides the modal. If the insertion is unsuccessful,
   * it sets `hasErrors` to true. Any unhandled errors during the operation are logged to the console.
   */
  async validateForm(data: any) {
    try {
      const {db_id, name, tags} = data;

      await this.fetchNewFood(new Food(db_id, name, tags));

      this.hasErrors = false;
      this.subFood?.push(this.retrieveFoodData());
      this.modalReference?.close();

    } catch (err) {
      this.hasErrors = true;
      const {error}: any = err;
      this.errorMessage = error.error;
    }
  }

  /**
   * This method returns a new Promise. If the Promise is resolved with a boolean value of true,
   * it indicates a successful insertion. If it is resolved with a boolean value of false,
   * it indicates an unsuccessful insertion. Any errors during the insertion process are propagated
   * by rejecting the Promise.
   * @param food {Food}
   */
  fetchNewFood(food: Food): Promise<Food> {
    food._tags = food._tags ? this.tagsArray : food._tags = [""];
    return new Promise((resolve, reject) => {
      this.subFood.push(this.alimentsService.insertFood(food).subscribe({
          next: (data) => {
            resolve(data);
          },
          error: (error) => {
            reject(error);
          }
        }
      ));
    });
  }

  retrieveFoodData() {
    return this.alimentsService.getAllFood().subscribe({
      next: data => {

        data.forEach((food: Food, index: number) => {
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

  saveData(indexDb: number, event: any) {
    const index = this.foodList.findIndex(food => food.aliment._db_id === indexDb);
    const newTags = event.target?.innerText.split(",").map((str: string) => str.trim()).filter((a: string) => a !== "");
    this.foodList[index].editable = false;
    const someChanges = newTags ? this.foodList[index].aliment._tags.some((a, index) => a !== newTags[index]) : false;
    const lenChange = newTags ? newTags.length !== this.foodList[index].aliment._tags.length : false;
    if ((someChanges || lenChange)) {
      this.foodList[index].aliment._tags = newTags;
      new Promise((resolve, reject) => {
        this.subFood.push(this.alimentsService.updateFood(this.foodList[index].aliment).subscribe({
          next: data => {
            resolve(data);
          },
          error: err => {
            reject(err);
          }
        }));
      }).then(() => {
        this.subFood.push(this.retrieveFoodData());
      })
        .catch(err => console.error("An error has occurs", err));
    } else {
      event.target.innerText = newTags.toString();
    }
  }

}
