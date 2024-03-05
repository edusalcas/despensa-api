import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {AlimentsComponent} from "./aliments/aliments.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { IndexComponent } from './index/index.component';
import { AlimentsMainComponent } from './aliments/aliments-main/aliments-main.component';
import {HttpClientModule, provideHttpClient, withFetch} from "@angular/common/http";
import { RecipesComponent } from './recipes/recipes.component';
import { RecipesMainComponent } from './recipes/recipes-main/recipes-main.component';
import {NgOptimizedImage} from "@angular/common";

@NgModule({
  declarations: [
    AppComponent,
    AlimentsComponent,
    HeaderComponent,
    FooterComponent,
    IndexComponent,
    AlimentsMainComponent,
    RecipesComponent,
    RecipesMainComponent
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        ReactiveFormsModule,
        HttpClientModule,
        FormsModule,
        NgOptimizedImage
    ],
  providers: [
    provideClientHydration(),
    provideHttpClient(withFetch())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
