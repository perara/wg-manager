import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LayoutComponent } from '../layout/layout/layout.component';
import { ErrorComponent } from './error';
import { LoginComponent } from './user/login/login.component';
import { AuthGuard } from '@services/*';
import { EditComponent } from './user/edit/edit.component';

const routes: Routes = [
  { path: '', component: LayoutComponent, children:
  [
        { path: 'dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [AuthGuard] },
        { path: '404', component: ErrorComponent, pathMatch: 'full' },
  ],
  },
  { path: 'user', component: LayoutComponent, children:
  [
        { path: 'edit', component: EditComponent, pathMatch: 'full' },
        { path: 'login', component: LoginComponent, pathMatch: 'full' },
  ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PageRoutingModule { }
