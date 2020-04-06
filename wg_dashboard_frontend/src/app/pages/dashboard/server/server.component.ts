import {Component, Input, OnInit, Output} from '@angular/core';
import {Server} from "../../../interfaces/server";
import {ServerService} from "../../../services/server.service";
import {DataService} from "../../../services/data.service";

@Component({
  selector: 'app-server',
  templateUrl: './server.component.html',
  styleUrls: ['./server.component.scss']
})
export class ServerComponent implements OnInit {
  @Input() server: Server;
  @Input() servers: Array<Server>;
  serverConfig: string;

  constructor(private serverAPI: ServerService, private comm: DataService) { }

  ngOnInit(): void {

    this.serverAPI.serverConfig(this.server).subscribe((x: any) => this.serverConfig = x.config)

  }

  edit(){

    this.comm.emit('server-edit', this.server);
  }

  stop() {
    this.serverAPI.stopServer(this.server).subscribe((apiServer) => {
      this.server.is_running = apiServer.is_running
    })
  }

  start() {
    this.serverAPI.startServer(this.server).subscribe((apiServer) => {
      this.server.is_running = apiServer.is_running
    })
  }

  addPeer() {
    this.serverAPI.addPeer(this.server).subscribe((peer) => {
      this.server.peers.push(peer)
    })
  }

  restart() {
    this.serverAPI.restartServer(this.server).subscribe((apiServer) => {
      this.server.is_running = apiServer.is_running
    })
  }


  delete() {
    const index = this.servers.indexOf(this.server);
    this.serverAPI.deleteServer(this.server).subscribe((apiServer) => {
      this.servers.splice(index, 1);
    })
  }
}
