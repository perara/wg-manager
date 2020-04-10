import { Component, OnInit } from '@angular/core';
import { BreakpointObserver } from '@angular/cdk/layout';
import { Server } from '../../interfaces/server';
import { ServerService } from '../../services/server.service';
import { Peer } from '../../interfaces/peer';

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  servers: Server[] = [];

  constructor(private breakpointObserver: BreakpointObserver, private serverAPI: ServerService) {

  }

  ngOnInit(): void {
    this.serverAPI.getServers()
      .subscribe((servers: Server[]) => {
        this.servers.push(...servers);
        servers.forEach((server) => {

          this.serverAPI.serverStats(server).subscribe((stats: Peer[]) => {
            stats.forEach(item => {
              const peer = server.peers.find(x => x.public_key == item.public_key);
              peer._stats = item;
            });

          });

        });

      });
  }

}
