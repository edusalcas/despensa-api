import { Component } from '@angular/core';
import {IndexComponent} from "./components/index/index.component";
import {RouterOutlet} from "@angular/router";


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: true,
  imports: [RouterOutlet, IndexComponent],
  styleUrl: './app.component.css'
})
export class AppComponent {

}
