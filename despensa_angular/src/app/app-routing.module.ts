import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AlimentsComponent} from "./aliments/aliments.component";
import {IndexComponent} from "./index/index.component";

const routes: Routes = [
  { path: 'index', component: IndexComponent },
  { path: 'aliments', component: AlimentsComponent },
  { path: '', redirectTo: '/index', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
