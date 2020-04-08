import {Component, OnInit} from '@angular/core';
import { map } from 'rxjs/operators';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';
import {Server} from "../../interfaces/server";
import {ServerService} from "../../services/server.service";
import {Peer} from "../../interfaces/peer";

@Component({
  selector: 'dashboard2',
  templateUrl: './dashboard2.component.html',
  styleUrls: ['./dashboard2.component.css']
})
export class Dashboard2Component implements OnInit
{
  servers: Array<Server> = [];

  constructor(private breakpointObserver: BreakpointObserver, private serverAPI: ServerService) {

  }


  ngOnInit(): void {
    this.serverAPI.getServers()
      .subscribe( (servers: Array<Server>) => {
        this.servers.push(...servers);
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
