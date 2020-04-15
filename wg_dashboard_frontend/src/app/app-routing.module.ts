import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { LayoutModule } from './layout/layout.module';

import { ErrorComponent } from './page/error';

@NgModule({
  imports: [
    RouterModule.forRoot(
      [
        { path: '', redirectTo: 'page/dashboard', pathMatch: 'full' },
        { path: 'page',  loadChildren: () => import('./page/page.module').then(m => m.PageModule) },

        /*{ path: 'app', component: LayoutComponent, children:
            [
              //{ path: 'dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [AuthGuard]},
              { path: 'dashboard2', component: Dashboard2Component, pathMatch: 'full'},

              { path: '**', redirectTo: '/pages/404'},
            ]
        },*/

        /*{ path: 'user', component: LayoutComponent, children:
            [
              { path: 'login', component: LoginComponent, pathMatch: 'full'},
              { path: 'edit', component: EditComponent, pathMatch: 'full', canActivate: [AuthGuard]},
            ]
        },*/
        { path: '**', redirectTo: '/page/404' },

      ],
      { useHash: true },
    ),
    LayoutModule,
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}

