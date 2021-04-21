import { AbstractControl, ValidationErrors } from '@angular/forms';
import * as IPCIDR from 'ip-cidr';
import {Address4, Address6} from 'ip-address'

export class IPValidator {

  static isIPAddress(control: AbstractControl): ValidationErrors | null {

    try {
      new Address4(control.value)
      return null
    } catch (e) {}
    try{
      new Address6(control.value)
      return null
    } catch (e) {}
    return { validIP: true };
  }



}
