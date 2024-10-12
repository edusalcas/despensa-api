import {AfterViewInit, Component, EventEmitter, OnDestroy, OnInit, Output, TemplateRef, ViewChild} from '@angular/core';
import {FormsModule, NgForm} from "@angular/forms";
import {NgIf} from "@angular/common";
import {Subscription} from "rxjs";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {Food} from "../../../entities/food";
import {AlimentsService} from "../../../services/aliments.service";

@Component({
  selector: 'app-add-aliment',
  standalone: true,
  imports: [
    FormsModule,
    NgIf
  ],
  templateUrl: './add-aliment.component.html',
  styleUrl: './add-aliment.component.css'
})
export class AddAlimentComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('addFoodForm') addFoodForm: NgForm | undefined;
  protected tags = '';
  protected subs: Subscription[] = [];
  @Output() close = new EventEmitter<any>();
  @Output() confirm = new EventEmitter<any>();
  @ViewChild('modal')
  private modal: TemplateRef<any> | undefined;
  protected hasErrors: boolean = false;
  protected errorMessage!: string;


  constructor(private modalService: NgbModal,
              private alimentsService: AlimentsService) {
  }

  ngOnInit(): void {

  }

  ngOnDestroy(): void {
    this.subs?.forEach(sub => sub.unsubscribe());
  }

  ngAfterViewInit(): void {
    this.open()
  }

  get tagsArray() {
    return this.tags.split(',').map((tag: { trim: () => any; }) => tag.trim());
  }

  open() {
    this.modalService.open(this.modal, {centered: true, scrollable: true, backdrop: "static"}).result.then(
      (result) => {
        this.confirm.emit(result);
      },
      () => {
        this.close.emit();
      }
    );
  }

  /**
   * This method returns a new Promise. If the Promise is resolved with a boolean value of true,
   * it indicates a successful insertion. If it is resolved with a boolean value of false,
   * it indicates an unsuccessful insertion. Any errors during the insertion process are propagated
   * by rejecting the Promise.
   * @param food {Food}
   */
  private fetchNewFood(food: Food): Promise<Food> {
    return new Promise((resolve, reject) => {
      this.subs.push(this.alimentsService.insertFood(food).subscribe({
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

  /**
   * Validates the form and submits the new food item.
   *
   * This function is responsible for validating the form and submitting the new food item.
   * It first prevents the default action of the submit event.
   * Then, it checks if the tags are provided in the form value. If the tags are provided, it sets the tags to an array.
   * If the tags are not provided, it sets the tags to an empty array.
   * It then tries to cast the form value to a Food instance.
   * If the casting is successful, it fetches the new food item from the alimentsService.
   * If the fetching is successful, it sets the hasErrors property to false and closes the form with the new food item.
   * If the fetching fails, it sets the hasErrors property to true and sets the errorMessage to the error message.
   * If the casting is not successful, it sets the errorMessage to 'Unexpected error occurred'.
   *
   * @async
   * @param $event SubmitEvent - The submit event of the form.
   * @param form any - The form that is being submitted.
   * @param form_value any - The value of the form.
   * @throws Will set the errorMessage to the error message if the fetchNewFood function fails.
   * @throws Will set the errorMessage to 'Unexpected error occurred' if the casting of the form value to a Food instance fails.
   */
  async validateForm($event: SubmitEvent, form: any, form_value: any) {
    $event.preventDefault();
    form_value.tags = form_value.tags ? this.tagsArray : form_value.tags = [""];
    form_value = Food.cast(form_value);
    if (form_value instanceof Food) {
      try {
        const newFood = await this.fetchNewFood(form_value);
        this.hasErrors = false;
        form.close(newFood);
      } catch (err) {
        const {error}: any = err;
        this.hasErrors = true;
        this.errorMessage = error.error;
      }
    } else {
      this.errorMessage = 'Unexpected error occurred';
    }
  }
}
