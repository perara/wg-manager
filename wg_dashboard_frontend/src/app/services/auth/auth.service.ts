import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '../../../environments/environment';
import {User} from "../../interfaces/user";

const tokenName = 'token';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  public user: User = null;
  private url = `${environment.apiBaseUrl}/api`;

  constructor(private http: HttpClient) {}

  public get isLoggedIn(): boolean {
    return !!this.user?.access_token
  }

  public login(data): Observable<any> {
    // Create form
    let formData: FormData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);


    return this.http.post(`${this.url}/login`, formData)
      .pipe(
        map((res: any) => {
          this._handleUser(res);
        }));
  }

  public edit(formData: any){
    return this.http.post(`${this.url}/user/edit`, formData)
      .pipe(map((res: any) => {
        this._handleUser(res);
      }));
  }

  _handleUser(res: any){
    const user: any = res.user;
    user.access_token = res.access_token;
    user.token_type = res.token_type;
    localStorage.setItem("session", JSON.stringify(user));
    this.init();
  }

  public logout() {
    return this.http.get(`${this.url}/logout`)
      .pipe(map((data) => {
        this.clearData();
        return of(false);
      }));
  }


  public clearData(){
    this.user = null;
    localStorage.clear();

  }

  public get authToken(): string {
    return localStorage.getItem(tokenName);
  }


  public init() {
    this.user = JSON.parse(localStorage.getItem('session'));
  }
}
