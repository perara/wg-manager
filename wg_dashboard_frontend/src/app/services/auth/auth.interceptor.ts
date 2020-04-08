import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';

import { AuthService } from './auth.service';
import {tap} from "rxjs/operators";
import {Router} from "@angular/router";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService, private router: Router) {}

  public intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization token for full api requests
    if (request.url.includes('api') && this.auth.isLoggedIn) {
      request = request.clone({
        setHeaders: { Authorization: `Bearer ${this.auth.user.access_token}`},
      });
    }

    return next.handle(request).pipe( tap(() => {},
      (err: any) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status !== 401 && err.status !== 403) {
            return;
          }

          this.auth.clearData();
          this.router.navigate(['/page/user/login']);
        }
      }));
  }
}
