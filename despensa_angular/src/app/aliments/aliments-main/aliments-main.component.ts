import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {AlimentsService} from "../aliments_service/aliments.service";

@Component({
  selector: 'app-aliments-main',
  templateUrl: './aliments-main.component.html',
  styleUrl: './aliments-main.component.css'
})
export class AlimentsMainComponent {

  constructor(
    private router: Router,
    private alimentsService: AlimentsService
  ) {}

  redirectTo(page: string) {
    this.router.navigate([`/${page}`]);
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
  changeModalState(id: string) {
    const modal = document.getElementById(id);
    if (modal !== null) {
      if (modal.style.visibility === "visible") {
        modal.style.visibility = "hidden";
        return true;
      } else {
        modal.style.visibility = "visible";
        return false;
      }
    }else return false;
  }

  /**
   *
   * @param ids {string} the ID of the element
   */
   validateForm(ids: string[]) {
     let formOK: boolean = true;
     for (const id of ids) {
       const field = <HTMLInputElement> document.getElementById(id);
       if (field !== null && field !== undefined) {
         const name = field.value;
         if (name === "") {
           // Change the background color of the corresponding cells to red
           field.style.borderColor = "red";
           formOK = false;
         }
       }
     }
     if (formOK) {
       this.fetchNewFood();
       this.retrieveFoodData();
     }
   }

   fetchNewFood(){
     const db_id :number = 0;
     const food_name  = <HTMLInputElement> document.getElementById("food-name");
     const food_tags  = <HTMLInputElement> document.getElementById("food-tags");
     if (food_name && food_tags) {
        const tags = food_tags.value.split(",").map(tag => tag.trim());
        this.alimentsService.insertFood(db_id, food_name.value, tags);
     }
   }
   retrieveFoodData(){
     this.alimentsService.getFood().subscribe(data => {
       const tableBody = <HTMLElement> document.getElementById("food-table-body");
       data.forEach(food => {
         const row = document.createElement("tr");
         const nameCell = document.createElement("td");
         const tagsCell = document.createElement("td");
         const idCell = document.createElement("td");
         nameCell.textContent = food.name;
         tagsCell.textContent = food.tags.join(", ");
         idCell.textContent = String(food.db_id);
         row.appendChild(nameCell);
         row.appendChild(tagsCell);
         row.appendChild(idCell);
         tableBody.appendChild(row);
       });
     });
   }

}
