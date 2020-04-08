import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Dashboard2Component} from "./dashboard2.component";
import {MatGridListModule} from "@angular/material/grid-list";
import {MatCardModule} from "@angular/material/card";
import {MatMenuModule} from "@angular/material/menu";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {ServerComponent} from "./server/server.component";
import {MatExpansionModule} from "@angular/material/expansion";
import {AddServerComponent} from "./add-server/add-server.component";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {ComponentsModule} from "../components";
import {FlexModule} from "@angular/flex-layout";
import {MatTableModule} from "@angular/material/table";
import {PeerComponent} from "./peer/peer.component";
import {QRCodeModule} from "angularx-qrcode";



@NgModule({
  declarations: [
    Dashboard2Component,
    ServerComponent,
    AddServerComponent,
    PeerComponent
  ],
  imports: [
    CommonModule,
    MatGridListModule,
    MatCardModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    ComponentsModule,
    FlexModule,
    MatTableModule,
    FormsModule,
    QRCodeModule,

  ]
})
export class Dashboard2Module { }
