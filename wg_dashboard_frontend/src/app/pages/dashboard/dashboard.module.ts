import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import { ThemeModule } from 'theme';

import { DashboardComponent } from './dashboard.component';
import { PeerComponent } from './peer/peer.component';
import { ComponentsModule } from "../components";
import { AddServerComponent } from './add-server/add-server.component';
import { ServerComponent } from './server/server.component';
import {AppModule} from "../../app.module";
import {QRCodeModule} from "angularx-qrcode";

@NgModule({
    imports: [
        CommonModule,
        ThemeModule,
        FormsModule,
        ReactiveFormsModule,
        ComponentsModule,
        QRCodeModule
    ],
  declarations: [
    DashboardComponent,
    PeerComponent,
    AddServerComponent,
    ServerComponent,
  ],
  exports: [
  ],
})
export class DashboardModule { }
