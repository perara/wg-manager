import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AuthInterceptor, AuthService } from '@services/*';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ComponentsModule } from './pages/components';
import { DashboardModule } from './pages/dashboard';
import { VarDirective } from './directives/var.directive';
import { QRCodeModule } from 'angularx-qrcode';
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {UserModule} from "./pages/user/user.module";

@NgModule({
  declarations: [AppComponent, VarDirective],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ComponentsModule,
    DashboardModule,
    UserModule,
    HttpClientModule,
    NgbModule,
    QRCodeModule
  ],
  providers: [
    AuthService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    }
  ],
  bootstrap: [AppComponent],
  exports: [
    VarDirective
  ]
})
export class AppModule {}
