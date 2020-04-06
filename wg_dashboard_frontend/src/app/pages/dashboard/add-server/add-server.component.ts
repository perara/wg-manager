import {Component, Input, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {IPValidator} from "../../../validators/ip-address.validator";
import {NumberValidator} from "../../../validators/number.validator";
import {Server} from "../../../interfaces/server";
import {ServerService} from "../../../services/server.service";
import {DataService} from "../../../services/data.service";

@Component({
  selector: 'app-add-server',
  templateUrl: './add-server.component.html',
  styleUrls: ['./add-server.component.scss']
})
export class AddServerComponent implements OnInit {

  @Input() servers: Array<Server>;

  serverForm = new FormGroup({
    address: new FormControl('', [IPValidator.isIPAddress]),
    interface: new FormControl('', [Validators.required, Validators.minLength(3)]),
    listen_port: new FormControl('', [Validators.required, NumberValidator.stringIsNumber]),
    endpoint: new FormControl('', Validators.required),
    private_key: new FormControl('', [Validators.minLength(44), Validators.maxLength(44)]),
    public_key: new FormControl('', [Validators.minLength(44), Validators.maxLength(44)]),
    shared_key: new FormControl('', [Validators.minLength(44), Validators.maxLength(44)]),
    post_up: new FormControl(''),
    post_down: new FormControl(''),

    // Unused on backend
    is_running: new FormControl(false),
    peers: new FormControl([]),
  });
  isEdit: boolean = false;
  editServer: Server = null;

  constructor(private serverAPI: ServerService, private comm: DataService) { }

  ngOnInit(): void {

    this.comm.on("server-edit").subscribe( (data: Server) => {
      this.isEdit = true;
      this.serverForm.setValue(data);
      this.editServer = data;
    })

  }

  add(form: Server) {

    if(this.isEdit){
      const idx = this.servers.indexOf(this.editServer);
      this.serverAPI.editServer(this.editServer, form).subscribe((server: Server) => {
        this.servers[idx] = server;
      });

    } else {

      this.serverAPI.addServer(form).subscribe((server: Server) => {
        this.servers.push(server);
      });
    }

    this.isEdit = false;
    this.serverForm.reset();
    this.editServer = null;
  }

  getKeyPair() {
    this.serverAPI.getKeyPair().subscribe((kp: any) => {
      this.serverForm.patchValue({
        private_key: kp.private_key,
        public_key: kp.public_key
      })
    });
  }

  getPSK() {
    this.serverAPI.getPSK().subscribe((psk: any) => {
      this.serverForm.patchValue({
        shared_key: psk.psk
      })
    });
  }
}
