import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { IPValidator } from '../../../validators/ip-address.validator';
import { NumberValidator } from '../../../validators/number.validator';
import { Server } from '../../../interfaces/server';
import { ServerService } from '../../../services/server.service';
import { DataService } from '../../../services/data.service';
import Parser, {Property, Section, Sections} from "@jedmao/ini-parser";
import {Peer} from "../../../interfaces/peer";
import {forkJoin, from, Observable, of} from "rxjs";
import {concatAll, concatMap, filter, map, mergeAll, mergeMap, switchMap} from "rxjs/operators";
import {NotifierService} from "angular-notifier";
@Component({
  selector: 'app-add-server',
  templateUrl: './add-server.component.html',
  styleUrls: ['./add-server.component.scss', '../dashboard.component.css'],
})
export class AddServerComponent implements OnInit {

  @Input() servers: Server[];

  // Translates from wg configuration keywords to form and backend keywords
  wgConfTranslation = {
    "Address": "address",
    "PrivateKey": "private_key",
    "ListenPort": "listen_port",
    "PostUp": "post_up",
    "PostDown": "post_down",
    "PublicKey": "public_key",

    // Peer
    "Endpoint": "endpoint",
    "AllowedIPs": "allowed_ips",
    "DNS": "dns"
  }

  serverForm: FormGroup = null;
  isEdit = false;
  editServer: Server = null;

  initForm(){
    this.serverForm = new FormGroup({
      address: new FormControl('', [IPValidator.isIPAddress]),
      interface: new FormControl('', [Validators.required, Validators.minLength(3)]),
      listen_port: new FormControl('', [Validators.required, NumberValidator.stringIsNumber]),
      endpoint: new FormControl('', Validators.required),
      dns: new FormControl(''),
      private_key: new FormControl('' ),
      public_key: new FormControl('' ),
      post_up: new FormControl(''),
      post_down: new FormControl(''),

      // Unused on backend
      configuration: new FormControl(''),
      is_running: new FormControl(false),
      peers: new FormControl([]),
    });
  }

  constructor(private serverAPI: ServerService, private comm: DataService, private notify: NotifierService) {

  }

  ngOnInit(): void {
    this.initForm();

    this.comm.on('server-edit').subscribe((data: Server) => {
      this.isEdit = true;
      this.serverForm.patchValue(data);

      this.editServer = data;
    });

  }

  parseFiles($event){
    const files: File[] = $event.target.files;

    let observables = []
    Array.from(files).forEach( (file: File) => {

      let obs = from([file])
        .pipe(map(x => from(x.text())))
        .pipe(mergeMap(x => x))
        .pipe(map((x) => new Parser().parse(x).items))
        .pipe(map((x: Section[]) => x.filter(y => y.name !== "" && y.name != null)))
        .pipe(map( (x: Section[]) => {

          let data: any = {}
          // Store filename
          data.fileName = file.name;

          // Convert nodes to key-value dict
          x.forEach( (y: any) => {
            y.nodes = y.nodes.reduce((result, filter) => {
              result[this.wgConfTranslation[filter["key"]]] = filter["value"];
              return result;
            },{});
          })
          data.sections = x;

          // Look for endpoint in peer configuration. TODO - Better way?
          data.isClient = data.sections
            .filter( section => Object.keys(section.nodes).find( nk => nk === "endpoint"))
            .length > 0;

          // 'Detect' if its a client
          return data
        }));
      observables.push(obs);
    });

    forkJoin(observables).subscribe(data => {
      let server: any = data.filter((x: any) => !x.isClient);

      if(server.length !== 1) {
        // TODO output error - should only be one server
        this.notify.notify("error", "Detected multiple server files!")
        return false;
      }
      server = server[0];

      const peers = data.filter((x: any) => x.isClient);
      //console.log(peers)
      this.importProcessServer(server);
      peers.forEach( peer => {
        this.importProcessPeer(peer);
      })
    })

  }

  importProcessServer(server) {
    let iFace: any = server.sections.find(x => x.name == "Interface")
    const sPeers = server.sections.filter(x => x.name == "Peer");

    if(iFace === null){
      // TODO error out - should have [interface] on server
      this.notify.notify("error", "Could not find [Interface] section")
      return false;
    }

    iFace.nodes["peers"] = sPeers
      .map( x => x.nodes)
      .map( x => {
      x.server_id = -1;
      x.address = x.allowed_ips;  // Allowed_ips in server is the address of the peer (Seen from server perspective)
      x.allowed_ips = null;  // This should be retrieved from peer data config
      return x;
    })
    this.serverForm.patchValue({
      interface: server.fileName.replace(".conf", "")
    })
    this.serverForm.patchValue(iFace.nodes)


  }

  importProcessPeer(peer){
    let formPeers = this.serverForm.controls.peers.value;
    let iFace: any = peer.sections.find(x => x.name == "Interface")
    const sPeers = peer.sections.filter(x => x.name == "Peer");

    if(sPeers.length > 1) {
      // TODO not supported for multi-server peers
      this.notify.notify("error", "Multi-server peers are not supported! Peer " + peer.fileName +
        " will be imported partially.")

      return false;
    }
    let sPeer = sPeers[0];

    let formPeer = formPeers
      .find(x =>  x.address.split("/")[0] === iFace.nodes.address.split("/")[0])
    formPeer.name = peer.fileName;
    formPeer.private_key = iFace.nodes.private_key;
    formPeer.allowed_ips = sPeer.nodes.allowed_ips;
    formPeer.dns = iFace.nodes.dns;
    this.serverForm.patchValue({
      endpoint: sPeer.nodes.endpoint.split(":")[0],
      public_key: sPeer.nodes.public_key

    })
  }



  add(form: Server) {

    if (this.isEdit) {
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
    this.editServer = null;
    this.serverForm.reset();
    this.serverForm.clearValidators();
  }

  getKeyPair() {
    this.serverAPI.getKeyPair().subscribe((kp: any) => {
      this.serverForm.patchValue({
        private_key: kp.private_key,
        public_key: kp.public_key,
      });
    });
  }



  resetForm() {
    this.isEdit = false;
    this.editServer = null;

    this.initForm()
  }
}
