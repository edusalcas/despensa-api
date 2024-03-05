import {Component, Input} from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

  @Input() headerContent: string | undefined;

  @Input() navBar: {page:string, name:string}[] | undefined;

  @Input() login: boolean | undefined;
  constructor(private router: Router) {
  }

}
