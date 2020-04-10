import { AbstractControl, ValidationErrors } from '@angular/forms';
import * as IPCIDR from 'ip-cidr';

export class IPValidator {

  static isIPAddress(control: AbstractControl): ValidationErrors | null {
    if (!control.value  || !(new IPCIDR(control.value).isValid()) || !control.value.includes('/')) {
      return { validIP: true };
    }
    return null;
  }
}
