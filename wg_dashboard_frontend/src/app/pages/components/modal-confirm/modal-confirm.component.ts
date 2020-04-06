import {Component, EventEmitter, Input, OnInit, Output, ViewEncapsulation} from '@angular/core';
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-modal-confirm',
  templateUrl: './modal-confirm.component.html',
  encapsulation: ViewEncapsulation.None,
  styleUrls: ['./modal-confirm.component.scss']
})
export class ModalConfirmComponent implements OnInit{
  @Input() noConfirm: boolean = false;
  @Input() qrCode: boolean = false;
  @Input() icon: string;
  @Input() hover: string;
  @Input() title: string;
  @Input() text: string;
  @Input()  area: boolean;
  @Output() onCancel: EventEmitter<any> = new EventEmitter();
  @Output() onConfirm: EventEmitter<any> = new EventEmitter();
  constructor(public modal: NgbModal) {

  }

  open($event, content) {
    $event.stopPropagation();
    if(this.noConfirm) {
      this.onConfirm.emit();
      return true;
    }

    this.modal.open(content, {
      ariaLabelledBy: 'modal-basic-title',
      backdropClass: "light-blue-backdrop",
      windowClass: "dark-modal"
    }).result.then((result) => {
      if(result === "cancel"){
        this.onCancel.emit()
      }else if(result === "confirm"){
        this.onConfirm.emit();
      }

    }, (reason) => {

    });
  }

  ngOnInit(): void {

    this.area = this.area || false;
    this.area = !!this.area
  }




}
