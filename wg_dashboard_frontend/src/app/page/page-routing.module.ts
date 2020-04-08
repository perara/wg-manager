import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {Dashboard2Component} from "./dashboard2/dashboard2.component";
import {LayoutComponent} from "../layout/layout/layout.component";
import {ErrorComponent} from "./error";
import {LoginComponent} from "./user/login/login.component";
import {AuthGuard} from "@services/*";




const routes: Routes = [
  { path: '', component: LayoutComponent, children:
      [
        //{ path: 'dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [AuthGuard]},
        { path: 'dashboard', component: Dashboard2Component, pathMatch: 'full', canActivate: [AuthGuard]},
        { path: '404', component: ErrorComponent, pathMatch: 'full' },
      ]
  },
  { path: 'user', component: LayoutComponent, children:
      [
        //{ path: 'dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [AuthGuard]},
        { path: 'login', component: LoginComponent, pathMatch: 'full'},
      ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PageRoutingModule { }
