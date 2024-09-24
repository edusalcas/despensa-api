import { ComponentRef, Injectable, Type, ViewContainerRef} from '@angular/core';
import {Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ModalService {
  private componentRef!: ComponentRef<any>;
  private componentSubscriber!: Subject<object>;


  constructor() {
  }

  openModal(entry: ViewContainerRef, component: Type<any>, data?: any) {
    this.componentRef = entry.createComponent(component);

    if (data) {
      this.componentRef.instance['data'] = data;
    }

    this.componentRef.instance.close?.subscribe(() => this.closeModal());
    this.componentRef.instance.confirm?.subscribe((data: object) => this.confirm(data));

    this.componentSubscriber = new Subject<object>();
    return this.componentSubscriber.asObservable();

  }

  closeModal() {
    this.componentSubscriber.complete();
    this.componentRef.destroy();
  }

 confirm(data: object) {
  if (this.componentSubscriber) {
    this.componentSubscriber.next(data);
  }
  this.closeModal();
}
}
