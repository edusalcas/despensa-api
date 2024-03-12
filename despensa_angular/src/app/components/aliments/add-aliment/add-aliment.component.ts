import {AfterViewInit, Component, EventEmitter, OnDestroy, OnInit, Output, TemplateRef, ViewChild} from '@angular/core';
import {FormsModule, NgForm} from "@angular/forms";
import {NgIf} from "@angular/common";
import {Subscription} from "rxjs";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {Food} from "../../../entities/food";
import {AlimentsService} from "../../../services/aliments_service/aliments.service";

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

  async validateForm($event: SubmitEvent, form: any, form_value: any) {
    $event.preventDefault();
    form_value.tags = form_value.tags ? this.tagsArray : form_value.tags = [""];
    form_value = Food.cast(form_value);
    if (form_value instanceof Food) {
      try {
        await this.fetchNewFood(form_value);
        this.hasErrors = false;
        form.close(form_value);
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
