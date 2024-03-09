import {ComponentFactoryResolver, ComponentRef, Injectable, Type, ViewContainerRef} from '@angular/core';
import {Subject} from "rxjs";
import {AddRecipeComponent} from "../../components/recipes/recipes-main/add-recipe/add-recipe.component";

@Injectable({
  providedIn: 'root'
})
export class AddRecipeService {
  private componentRef!: ComponentRef<any>;
  private componentSubscriber!: Subject<string>;


  constructor() {
  }

  openModal(entry: ViewContainerRef) {
    this.componentRef = entry.createComponent(AddRecipeComponent);

    this.componentRef.instance.close.subscribe(() => this.closeModal());
    this.componentRef.instance.confirm.subscribe((data: any) => this.confirm(data));

    this.componentSubscriber = new Subject<string>();
    return this.componentSubscriber.asObservable();

  }

  closeModal() {
    this.componentSubscriber.complete();
    this.componentRef.destroy();
  }

  confirm(data: any) {
    this.componentSubscriber.next(data);
    this.closeModal();
  }
}
