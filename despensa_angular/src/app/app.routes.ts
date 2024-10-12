import { Routes } from '@angular/router';

export const routes: Routes = [
  {path: 'index', loadComponent: () => import('./components/index/index.component').then(m => m.IndexComponent)},
  {path: 'aliments', loadComponent: () => import('./components/aliments/aliments-main/aliments-main.component').then(m => m.AlimentsMainComponent)},
  {path: 'recipes',
    children: [
      {path: '', loadComponent: () => import('./components/recipes/recipes-main/recipes-main.component').then(m => m.RecipesMainComponent)},
      { path: 'details/:id' , loadComponent: () => import('./components/recipes/details/details.component').then(m => m.DetailsComponent)},
    ]
  },
  {path: '', redirectTo: '/index', pathMatch: 'full' as const}
];
