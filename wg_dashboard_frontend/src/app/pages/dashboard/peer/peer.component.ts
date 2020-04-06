import {Component, Input, OnInit} from '@angular/core';
import {ServerService} from "../../../services/server.service";
import {Peer} from "../../../interfaces/peer";
import {Server} from "../../../interfaces/server";

@Component({
  selector: 'app-peer',
  templateUrl: './peer.component.html',
  styleUrls: ['./peer.component.scss']
})
export class PeerComponent implements OnInit {

  @Input("peer") peer: Peer;
  @Input("server") server: Server;

  config: string = "Loading...";


  constructor(public serverAPI: ServerService) { }

  ngOnInit(): void {
  }

  edit(){
    if(this.peer._edit) {

      // Submit the edit (True -> False)
      const idx = this.server.peers.indexOf(this.peer);
      this.serverAPI.editPeer(this.peer).subscribe((newPeer) => {
        this.server.peers[idx] = newPeer;
      });

    } else if(!this.peer._edit) {
      this.peer._expand = true;

      // Open for edit. aka do nothing (False -> True

    }

    this.peer._edit = !this.peer._edit;


  }

  delete(){
    const idx = this.server.peers.indexOf(this.peer);
    this.serverAPI.deletePeer(this.peer).subscribe((apiServer) => {
      this.server.peers.splice(idx, 1);
    })
  }

  fetchConfig() {
    this.serverAPI.peerConfig(this.peer).subscribe((config: any) => {
      this.config = config.config
    })
  }

  pInt(string: string) {
    return parseInt(string)
  }
}
