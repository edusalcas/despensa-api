import {Component, ElementRef, OnInit, Renderer2, ViewChild} from '@angular/core';
import {Router} from "@angular/router";
import {AlimentsService} from "../aliments_service/aliments.service";
import {Food} from "../entities/food";
import {NgForm} from "@angular/forms";

@Component({
  selector: 'app-aliments-main',
  templateUrl: './aliments-main.component.html',
  styleUrl: './aliments-main.component.css'
})
export class AlimentsMainComponent implements OnInit{

  @ViewChild( 'addFoodForm') addFoodForm : NgForm | undefined;
  tags = '';

  foodList:Array<Food> = [];

  isModalHidden:boolean = true;

  mensajeError:string = '';

  get tagsArray() {
    return this.tags.split(',').map(tag => tag.trim());
  }


  constructor(
    private router: Router,
    private alimentsService: AlimentsService,
  ) {}

  ngOnInit(){
    this.retrieveFoodData();
  }

  /**
   * This method returns true or false depending on whether the element is switched to visible
   * or hidden
   *
   * @param id {string} the ID of the element for which you want to change visibility
   * @return true when the element is switched to hidden
   * @return false if the element is switched to visible or the element is not found,
   * which means its value is null
   */
  changeModalState() {
    this.isModalHidden = !this.isModalHidden;

    if(!this.isModalHidden){
      this.addFoodForm?.reset();
    }
  }

  /**
   *
   * @param data
   */
   async validateForm(data:Food) {
       try{
         const insertExitoso = await this.fetchNewFood(data);
         if (insertExitoso) {
           this.mensajeError = '';
           this.retrieveFoodData();
           this.changeModalState();
         } else {
           this.mensajeError = "The food name is already in use";
         }
       }catch(err){
           console.log(err);
       }
   }

   fetchNewFood(food:Food):Promise<boolean>{
     food.tags = this.tagsArray;
      return new Promise((resolve, reject) => {
        this.alimentsService.insertFood(food).subscribe({
            next: data => {
              data ? console.info("todo correcto") : console.warn("algo fue mal en BD");
              resolve(data);
            },
            error: error => {
              console.error("Error al insertar alimento", error);
              reject(error);
            }
          }
        );
      });
   }
   retrieveFoodData(){
     this.alimentsService.getAllFood().subscribe(data => {
        this.foodList = [...data];
     });
   }
}
