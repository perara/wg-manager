import {
  Component,
  ContentChild,
  EventEmitter,
  Input,
  OnInit,
  Output,
  TemplateRef, ViewChild, ViewContainerRef,
  ViewEncapsulation
} from '@angular/core';
import {NgForOfContext} from "@angular/common";

@Component({
  selector: 'app-modal-confirm',
  templateUrl: './modal-confirm.component.html',
  encapsulation: ViewEncapsulation.Emulated,
  styleUrls: ['./modal-confirm.component.scss'],
})
export class ModalConfirmComponent implements OnInit {
  @Input() noConfirm = false;
  @Input() qrCode = false;
  @Input() icon: string;
  @Input() hover: string;
  @Input() title: string;
  @Input() text: string;
  @Input()  area: boolean;
  @Output() onCancel: EventEmitter<any> = new EventEmitter();
  @Output() onConfirm: EventEmitter<any> = new EventEmitter();

  @ViewChild('modal', { read: TemplateRef }) _template: TemplateRef<any>;
  @ViewChild('vc', {read: ViewContainerRef}) vc: ViewContainerRef;
  shown = false;

  constructor() {


  }

  open($event){
    if (this.noConfirm) {
      this.onConfirm.emit($event);
      return true;
    }

    this.shown = true;
    //this.vc.createEmbeddedView(this._template, {fromContext: 'John'});

  }
  confirm($event){
    $event.stopPropagation();
    this.onConfirm.emit($event);
    this.shown=  false;

  }

  cancel($event){
    this.onCancel.emit($event);
    this.shown = false
  }

  ngOnInit(): void {

    this.area = this.area || false;
    this.area = !!this.area;
  }

}
