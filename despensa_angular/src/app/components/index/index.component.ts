import { Component } from '@angular/core';
import {FooterComponent} from "../footer/footer.component";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  standalone: true,
  imports: [
    FooterComponent,
    HeaderComponent
  ]
})
export class IndexComponent {

}
