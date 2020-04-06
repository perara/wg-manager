import { Injectable } from '@angular/core';
import {ConfigService} from "./config.service";
import {HttpClient} from "@angular/common/http";

import {catchError} from "rxjs/operators";
import {Server} from "../interfaces/server";
import {Peer} from "../interfaces/peer";
import {Observable, Subscribable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ServerService {
  public_url_wg: string = "/api/wg";
  public url: string = this.public_url_wg + "/server";
  constructor(private config: ConfigService, private http: HttpClient) {



  }

  public deletePeer(peer: Peer): Subscribable<Peer>{
    return this.http.post(this.url + "/peer/delete", peer)
  }


  public serverPerformAction(action: string, item: any): Subscribable<Server> {
    return this.http.post(this.url + "/" + action, item)
      .pipe(catchError(this.config.handleError.bind(this)))
  }

  public addPeer(server: Server): Subscribable<Peer>{
    return this.http.post(this.url + "/peer/add", server)
  }

  public editPeer(peer: Peer): Subscribable<Peer>{
    return this.http.post(this.url + "/peer/edit", peer)
  }

  public getServers(): Observable<Array<Server>>{
    return this.http.get<Array<Server>>(this.url + "/all")
      .pipe(catchError(this.config.handleError.bind(this)))
  }


  public addServer(item: Server): Subscribable<Server> {
    return this.http.post(this.url + "/add", item)
      .pipe(catchError(this.config.handleError.bind(this)))
  }

  public startServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction("start", item)
  }

  public stopServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction("stop", item)
  }

  public restartServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction("restart", item)
  }

  public deleteServer(item: Server): Subscribable<Server> {
    return this.serverPerformAction("delete", item)
  }

  public editServer(oldServer: Server, newServer: Server): Subscribable<Server> {
    return this.serverPerformAction("edit", {
      "interface": oldServer.interface,
      "server": newServer
    })
  }

  public getKeyPair() {
    return this.http.get(this.public_url_wg + "/generate_keypair")
  }

  public getPSK() {
    return this.http.get(this.public_url_wg + "/generate_psk")
  }

  public peerConfig(peer: Peer) {
    return this.http.post(this.public_url_wg + "/server/peer/config", peer)
  }

  public serverConfig(server: Server) {
    return this.http.post(this.url + "/config", server)
  }

  public serverStats(server: Server) {
    return this.http.post(this.url + "/stats", server)
  }
}
