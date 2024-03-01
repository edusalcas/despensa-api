import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {AlimentsComponent} from "./aliments/aliments.component";
import {ReactiveFormsModule} from "@angular/forms";
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { IndexComponent } from './index/index.component';
import { AlimentsMainComponent } from './aliments/aliments-main/aliments-main.component';

@NgModule({
  declarations: [
    AppComponent,
    AlimentsComponent,
    HeaderComponent,
    FooterComponent,
    IndexComponent,
    AlimentsMainComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule
  ],
  providers: [
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
