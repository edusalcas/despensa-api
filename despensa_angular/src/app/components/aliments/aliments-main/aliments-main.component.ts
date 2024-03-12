import {Component, OnDestroy, OnInit, ViewChild, ViewContainerRef} from '@angular/core';
import {AlimentsService} from "../../../services/aliments_service/aliments.service";
import {FormsModule} from "@angular/forms";
import {Food} from "../../../entities/food";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {Subscription} from "rxjs";
import {ModalService} from "../../../services/modal-service/modal.service";
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

          }
        }
      }
    }));
  }
}
