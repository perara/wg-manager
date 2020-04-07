import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EditComponent } from './edit/edit.component';
import {ReactiveFormsModule} from "@angular/forms";
import {CardModule} from "../../../theme/components/card";
import { LoginComponent } from './login/login.component';



@NgModule({
  declarations: [
    EditComponent,
    LoginComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    CardModule
  ]
})
export class UserModule {

}
