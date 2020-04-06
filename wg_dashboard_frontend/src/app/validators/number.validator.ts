import { AbstractControl, ValidationErrors } from '@angular/forms';
import * as IPCIDR from "ip-cidr";

export class NumberValidator {

  static stringIsNumber(control: AbstractControl) : ValidationErrors | null {
    if(isNaN(control.value)){
      return {validNumber: true}
    }
    return null;
  }
}
