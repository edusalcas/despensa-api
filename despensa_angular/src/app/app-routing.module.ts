import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AlimentsComponent} from "./aliments/aliments.component";
import {IndexComponent} from "./index/index.component";
import {RecipesComponent} from "./recipes/recipes.component";

const routes: Routes = [
  { path: 'index', component: IndexComponent },
  { path: 'aliments', component: AlimentsComponent },
  { path: 'recipes', component: RecipesComponent },
  { path: '', redirectTo: '/index', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
