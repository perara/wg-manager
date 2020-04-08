import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "@services/*";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  public loginForm: FormGroup;
  public username;
  public password;
  public error: string;

  constructor(private authService: AuthService,
              private fb: FormBuilder,
              private router: Router) {


    this.loginForm = this.fb.group({
      password: new FormControl('', Validators.required),
      username: new FormControl('', [
        Validators.required,
      ]),
    });
    this.username = this.loginForm.get('username');
    this.password = this.loginForm.get('password');
  }

  public ngOnInit() {
    this.authService.logout();
    this.loginForm.valueChanges.subscribe(() => {
      this.error = null;
    });
  }

  public login() {
    this.error = null;
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.getRawValue())
        .subscribe(res => this.router.navigate(['/page/dashboard']),
          error => this.error = error.message);
    }
  }

  public onInputChange(event) {
    event.target.required = true;
  }

}
