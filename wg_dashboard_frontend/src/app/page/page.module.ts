import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {PageRoutingModule} from "./page-routing.module";
import {Dashboard2Module} from "./dashboard2/dashboard2.module";
import {LoginComponent} from "./user/login/login.component";
import {MatCardModule} from "@angular/material/card";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";


@NgModule({
  declarations: [LoginComponent],
  imports: [
    CommonModule,
    PageRoutingModule,
    FormsModule,
    Dashboard2Module,
    MatCardModule,
    ReactiveFormsModule,
    MatInputModule,
  ],

})
export class PageModule { }
