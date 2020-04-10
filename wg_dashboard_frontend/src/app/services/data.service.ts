import { EventEmitter, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {

  _observables: any  = {};
  constructor() {}

  emit(event: string, value: any): void {
    if (this._observables.hasOwnProperty(event)) {
      this._observables[event].emit(value);
    }
  }

  on(event: string): Observable<any> {
    if (!this._observables.hasOwnProperty(event)) {
      this._observables[event] = new EventEmitter<any>();
    }

    return this._observables[event].asObservable();
  }

}
