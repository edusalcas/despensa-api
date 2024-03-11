import {Component, OnDestroy, OnInit} from '@angular/core';
import {HeaderComponent} from "../../header/header.component";
import {FooterComponent} from "../../footer/footer.component";
import {NgClass, NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {Recipe} from "../../../entities/recipe";
import {ActivatedRoute, RouterLink} from "@angular/router";
import {RecipesService} from "../../../services/recipes_service/recipes.service";
import {Subscription} from "rxjs";
import {
  NgbAccordionBody,
  NgbAccordionCollapse,
  NgbAccordionDirective,
  NgbAccordionHeader,
  NgbAccordionItem, NgbAccordionToggle, NgbCollapse,
  NgbDropdownAnchor
} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-details',
  standalone: true,
  imports: [
    HeaderComponent,
    FooterComponent,
    NgOptimizedImage,
    NgForOf,
    NgIf,
    NgbAccordionDirective,
    NgbAccordionHeader,
    NgbAccordionItem,
    NgbDropdownAnchor,
    NgbAccordionCollapse,
    NgbAccordionBody,
    NgbCollapse,
    NgClass,
    NgbAccordionToggle,
    RouterLink
  ],
  templateUrl: './details.component.html',
  styleUrl: './details.component.css'
})
export class DetailsComponent implements OnInit, OnDestroy{
  protected recipe: Recipe | undefined;
  private subRouter: Subscription | undefined;
  private subRecServ: Subscription | undefined;
  protected isPanelIngOpen: boolean = false;
  protected isPanelStpsOpen: boolean = false;

  constructor(private router:ActivatedRoute,
              private recipeService: RecipesService,
              ) {
  }

  ngOnInit() {
    let id = -1;
    this.subRouter = this.router.params.subscribe({
      next: value => {
        id = value["id"];
      }
    });

    this.subRecServ = this.recipeService.get(id).subscribe({
      next: data => {
        const time = data._time;
        data._time = time ? (time.toString().endsWith("min") ? time : time.toString().endsWith("mins") ? time : time.toString().concat("min")) : "0mins";
        this.recipe = data;
      },
      error: err => {
        console.error(err);
      }
    });
  }

  ngOnDestroy() {
    this.subRouter?.unsubscribe();
    this.subRecServ?.unsubscribe();
  }

}
