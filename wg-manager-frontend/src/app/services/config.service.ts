import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { throwError } from 'rxjs';
import {NotifierService} from "angular-notifier";

@Injectable({
  providedIn: 'root',
})
export class ConfigService {

  public applicationName = 'WireGuard Manager';

  constructor(private notify: NotifierService) {
  }

  public handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
      this.notify.notify("error", error.error.message)
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
      this.notify.notify("error", error.error.detail)
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  }
}
