import { Routes } from '@angular/router';

export const routes: Routes = [
  {path: 'index', loadComponent: () => import('./components/index/index.component').then(m => m.IndexComponent)},
  {path: 'aliments', loadComponent: () => import('./components/aliments/aliments.component').then(m => m.AlimentsComponent)},
  {path: 'recipes', loadComponent: () => import('./components/recipes/recipes.component').then(m => m.RecipesComponent)},
  {path: '', redirectTo: '/index', pathMatch: 'full' as const}
];
