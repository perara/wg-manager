import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "@services/*";
import {Router} from "@angular/router";

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.scss']
})
export class EditComponent implements OnInit {

  public editForm: FormGroup = new FormGroup({
    full_name: new FormControl(''),
    password: new FormControl('', Validators.required),
    email: new FormControl('', [
      Validators.required,
      Validators.pattern('^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$'),
      Validators.maxLength(20),
    ]),
    username: new FormControl('', [Validators.required, Validators.maxLength(20)]),
  });
  public user: any;
  public error: string;

  constructor(private authService: AuthService,
              private router: Router) {

  }

  public ngOnInit() {
    this.user = this.authService.user;


    this.editForm.setValue({
      full_name: this.user.full_name,
      password: "",
      email: this.user.email,
      username: this.user.username
    })
  }

  public edit() {
    if (this.editForm.valid) {
      this.authService.edit(this.editForm.getRawValue())
        .subscribe(res => this.router.navigate(['/app/dashboard']),
          error => this.error = error.message);
    }
  }

}
