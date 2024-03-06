import {Component, Input} from '@angular/core';
import {RouterLink} from "@angular/router";
import {NgForOf, NgIf} from "@angular/common";



@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  standalone: true,
  imports: [
    RouterLink,
    NgIf,
    NgForOf
  ],
  styleUrl: './header.component.css'
})
export class HeaderComponent {

  @Input() headerContent: string | undefined;

  @Input() navBar: {page:string, name:string}[] | undefined;

  @Input() login: boolean | undefined;

}
