import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ThemeModule } from 'theme';
import { ComponentsComponent } from './components.component';

import { ModalConfirmComponent } from './modal-confirm';
import { QRCodeModule } from 'angularx-qrcode';
import {MatButtonModule} from "@angular/material/button";
import {MatTooltipModule} from "@angular/material/tooltip";
import {MatCardModule} from "@angular/material/card";
import {MatIconModule} from "@angular/material/icon";
import {FlexModule} from "@angular/flex-layout";

@NgModule({
  imports: [
    CommonModule,
    ThemeModule,
    FormsModule,
    QRCodeModule,
    MatButtonModule,
    MatTooltipModule,
    MatCardModule,
    MatIconModule,
    FlexModule,
  ],
  providers: [
  ],
  exports: [
    ComponentsComponent,
    ModalConfirmComponent,
  ],
  declarations: [
    ComponentsComponent,
    ModalConfirmComponent,
  ],
})
export class ComponentsModule { }
