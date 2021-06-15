import { AbstractControl, ValidationErrors } from '@angular/forms';
import * as IPCIDR from 'ip-cidr';
import {Address4, Address6} from 'ip-address'

export class IPValidator {

  static isIPAddress(control: AbstractControl): ValidationErrors | null {
    if (Address4.isValid(control.value) || Address6.isValid(control.value))
      return null;
    else
      return { validIP: true };
  }



}
