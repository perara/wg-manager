import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PageRoutingModule } from './page-routing.module';
import { DashboardModule } from './dashboard/dashboard.module';
import { LoginComponent } from './user/login/login.component';
import { MatCardModule } from '@angular/material/card';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { FlexModule } from '@angular/flex-layout';
import { EditComponent } from './user/edit/edit.component';
import { MatButtonModule } from '@angular/material/button';
import {MatTableModule} from "@angular/material/table";
import { ApiKeyComponent } from './user/edit/api-key/api-key.component';

@NgModule({
  declarations: [LoginComponent, EditComponent, ApiKeyComponent],
  imports: [
    CommonModule,
    PageRoutingModule,
    FormsModule,
    DashboardModule,
    MatCardModule,
    ReactiveFormsModule,
    MatInputModule,
    FlexModule,
    MatButtonModule,
    MatTableModule,
  ],

})
export class PageModule { }
