import {Component, HostBinding, OnInit} from '@angular/core';

import { UpgradableComponent } from 'theme/components/upgradable';
import {AbstractControl, FormControl, FormGroup, NgForm, Validators} from "@angular/forms";
// goog-webfont-dl -o src/theme/fonts/font-roboto.css -p assets/fonts/Roboto -d src/assets/fonts/Roboto -a Roboto

import * as IPCIDR from "ip-cidr";
import {Server} from "../../interfaces/server";
import {ServerService} from "../../services/server.service";

import {Peer} from "../../interfaces/peer";
import {IPValidator} from "../../validators/ip-address.validator";




@Component({
  selector: 'app-dashboard',
  styleUrls: ['./dashboard.component.scss', './accordion.scss'],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent extends UpgradableComponent implements OnInit
{
  @HostBinding('class.mdl-grid') private readonly mdlGrid = true;
  @HostBinding('class.mdl-grid--no-spacing') private readonly mdlGridNoSpacing = true;

  servers: Array<Server> = [];

  constructor(private serverAPI: ServerService) {
    super();
  }

  ngOnInit(): void {
    this.serverAPI.getServers()
      .subscribe( (servers: Array<Server>) => {
        this.servers.push(...servers)
        servers.forEach((server) => {

          this.serverAPI.serverStats(server).subscribe((stats: Peer[]) => {
            stats.forEach( item => {
              const peer = server.peers.find(x => x.public_key == item.public_key);
              peer._stats = item
            });


          });


        });


      })
  }

}
