import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LayoutComponent } from './layout/layout.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { FlexLayoutModule } from '@angular/flex-layout';
import { RouterModule } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import {MatSlideToggleModule} from "@angular/material/slide-toggle";

@NgModule({
  declarations: [LayoutComponent],
    imports: [
        CommonModule,
        MatSidenavModule,
        MatToolbarModule,
        MatListModule,
        MatIconModule,
        MatButtonModule,
        FlexLayoutModule,
        RouterModule,
        MatMenuModule,
        MatSlideToggleModule,
    ],
  exports: [

  ],
})
export class LayoutModule { }
