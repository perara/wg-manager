import { Component, EventEmitter, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { ServerService } from '../../../services/server.service';
import { Peer } from '../../../interfaces/peer';
import { Server } from '../../../interfaces/server';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-peer',
  templateUrl: './peer.component.html',
  encapsulation: ViewEncapsulation.None,
  styleUrls: ['./peer.component.scss'],
})
export class PeerComponent implements OnInit {

  @Input('peer') peer: Peer;
  @Input('server') server: Server;
  @Input('selectedPeer') selectedPeer: Peer;
  @Input('onEvent') editPeerEmitter: EventEmitter<any> = new EventEmitter<any>();

  constructor(public serverAPI: ServerService) { }

  ngOnInit(): void {

    this.editPeerEmitter.subscribe((msg) => {
      if (msg.peer !== this.peer) {
        return;
      }
      if (msg.type === 'edit') {
        this.edit();

      } else if (msg.type == 'delete') {
        this.delete();
      }
    });

  }

  edit() {
    if (this.peer._edit) {


      // Submit the edit (True -> False)
      const idx = this.server.peers.indexOf(this.peer);
      this.serverAPI.editPeer(this.peer).subscribe((data) => {
        this.server.configuration = data.server_configuration;
        Object.keys(data.peer).forEach(k => {
          this.server.peers[idx][k] = data.peer[k];
        });
      });

    } else if (!this.peer._edit) {
      this.peer._expand = true;

      // Open for edit. aka do nothing (False -> True

    }

    this.peer._edit = !this.peer._edit;

  }

  delete() {
    const idx = this.server.peers.indexOf(this.peer);
    this.serverAPI.deletePeer(this.peer).subscribe((apiServer) => {
      this.server.peers.splice(idx, 1);
    });
  }

  getPSK() {
    this.serverAPI.getPSK().subscribe((psk: any) => {
      this.peer.shared_key = psk.psk;
    });
  }

}
