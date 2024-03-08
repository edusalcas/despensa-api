import {Injectable} from '@angular/core';
import {Ingredient} from "../../entities/ingredient";
import {AlimentsService} from "../aliments_service/aliments.service";

@Injectable({
  providedIn: 'root'
})
export class IngredientsService {

  constructor(
    private alimentsService: AlimentsService
  ) {
  }

  public castAsIngredient(ingredient: any) {

    let {aliment, quantity, quantity_type, optional, db_id} = ingredient;
    optional = optional === 1;
    aliment = this.alimentsService.castAsFood(aliment);

    return new Ingredient(aliment, quantity, quantity_type, optional, db_id);
  }

}
