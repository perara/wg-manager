import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { LayoutsModule } from './layouts';
import { CommonLayoutComponent } from './layouts/common-layout';
import { DashboardComponent } from './pages/dashboard';

import {AuthGuard} from "@services/*";
import {EditComponent} from "./pages/user/edit/edit.component";
import {LoginComponent} from "./pages/user/login/login.component";



@NgModule({
  imports: [
    RouterModule.forRoot(
      [
        { path: '', redirectTo: 'app/dashboard', pathMatch: 'full' },
        { path: 'app', component: CommonLayoutComponent, children:
            [
              { path: 'dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [AuthGuard]},


              { path: '**', redirectTo: '/pages/404'},
            ]
        },

        { path: 'user', component: CommonLayoutComponent, children:
            [
              { path: 'login', component: LoginComponent, pathMatch: 'full'},
              { path: 'edit', component: EditComponent, pathMatch: 'full', canActivate: [AuthGuard]},
            ]
        },


        { path: '**', redirectTo: '/pages/404' },
      ],
      { useHash: true },
    ),
    LayoutsModule,
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
