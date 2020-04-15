import { Injectable } from '@angular/core';
import { ConfigService } from './config.service';
import { HttpClient } from '@angular/common/http';

import { catchError } from 'rxjs/operators';
import { Server } from '../interfaces/server';
import { Peer } from '../interfaces/peer';
import { Observable, Subscribable } from 'rxjs';
import {NotifierService} from "angular-notifier";

@Injectable({
  providedIn: 'root',
})
export class ServerService {
  public base = '/api/v1/';
  public serverURL = this.base + "server";
  public peerURL = this.base + "peer";
  public wgURL = this.base + "wg";


  constructor(private config: ConfigService, private http: HttpClient, private notify: NotifierService) {

  }

  public deletePeer(peer: Peer): Subscribable<Peer> {
    return this.http.post(this.peerURL + '/delete', peer);
  }

  public serverPerformAction(action: string, item: any): Subscribable<Server> {
    return this.http.post(this.serverURL + '/' + action, item)
      .pipe(catchError(this.config.handleError));
  }

  public addPeer(server_interface: any): Subscribable<Peer> {
    return this.http.post(this.peerURL + '/add', server_interface);
  }

  public editPeer(peer: Peer): Subscribable<{ peer: Peer, server_configuration: string }> {
    return this.http.post(this.peerURL + '/edit', peer);
  }

  public getServers(): Observable<Server[]> {
    return this.http.get<Server[]>(this.serverURL + '/all')
      .pipe(catchError(this.config.handleError.bind(this)));
  }

  public addServer(item: Server): Subscribable<Server> {
    return this.http.post(this.serverURL + '/add', item)
      .pipe(catchError(this.config.handleError.bind(this)));
  }

  public startServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction('start', item);
  }

  public stopServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction('stop', item);
  }

  public restartServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction('restart', item);
  }

  public deleteServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction('delete', item);
  }

  public editServer(oldServer: Server, newServer: Server): Subscribable<Server> {
    return this.serverPerformAction('edit', {
      interface: oldServer.interface,
      server: newServer,
    });
  }

  public getKeyPair() {
    return this.http.get(this.wgURL + '/generate_keypair');
  }

  public getPSK() {
    return this.http.get(this.wgURL + '/generate_psk');
  }

  public peerConfig(peer: Peer) {
    return this.http.post(this.peerURL + '/config', peer);
  }

  public serverConfig(server: Server) {
    return this.http.post(this.serverURL + '/config', server);
  }

  public serverStats(server: Server) {
    return this.http.post(this.serverURL + '/stats', server);
  }
}
