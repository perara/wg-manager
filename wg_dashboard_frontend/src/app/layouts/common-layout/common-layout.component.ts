import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '@services/*';

@Component({
  selector: 'app-common-layout',
  templateUrl: './common-layout.component.html',
})
export class CommonLayoutComponent implements OnInit {
  public title = 'Wireguard Manager';
  public menu = [
    { name: 'Dashboard', link: '/app/dashboard', icon: 'dashboard' },
  ];


  constructor(public auth: AuthService,
              public router: Router) {}

  public ngOnInit() {

  }

  public logout() {
    this.auth.logout()
      .subscribe(res => this.router.navigate(['/user/login']));
  }
}
