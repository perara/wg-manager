import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ThemeModule } from 'theme';
import { ComponentsComponent } from './components.component';

import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ModalConfirmComponent} from "./modal-confirm";
import {QRCodeModule} from "angularx-qrcode";

@NgModule({
    imports: [
        CommonModule,
        ThemeModule,
        FormsModule,
        QRCodeModule
    ],
  providers: [
    NgbActiveModal
  ],
  exports: [
    ComponentsComponent,
    ModalConfirmComponent
  ],
  declarations: [
    ComponentsComponent,
    ModalConfirmComponent
  ],
})
export class ComponentsModule { }
