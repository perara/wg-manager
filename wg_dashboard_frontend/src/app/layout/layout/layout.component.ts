import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { map, shareReplay } from 'rxjs/operators';
import { ConfigService } from '../../services/config.service';
import { AuthService } from '@services/*';
import {OverlayContainer} from "@angular/cdk/overlay";
import {DataService} from "../../services/data.service";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss'],
})
export class LayoutComponent implements OnInit {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay(),
    );

  menu: {link: string[], icon: string, text: string}[] = [
    { link: ['/page/dashboard'], icon: 'home', text: 'Dashboard' },
  ];

  themes =  [
    {theme: "indigo-pink", name: "Blue"},
    {theme: "deeppurple-amber", name: "Purple"},
    {theme: "pink-bluegrey", name: "Pink"},
    {theme: "purple-green", name: "Purple-Green"},
  ];
  currentTheme = null;
  darkMode = false;

  constructor(
    private breakpointObserver: BreakpointObserver,
    public config: ConfigService,
    public auth: AuthService,
    private comm: DataService,
    private cookieService: CookieService
  ) {}
  ngOnInit(): void {
    console.log('Layout');

    if(this.cookieService.check("currentTheme")){
      this.currentTheme = JSON.parse(this.cookieService.get("currentTheme"));
      this.darkMode = (this.cookieService.get("darkMode") === 'true');
    }else {
      this.currentTheme = { ... this.themes[0]}
    }

  }

  toggleDarkMode($event){
    $event.stopPropagation();
    this.darkMode = !this.darkMode;
    this.cookieService.set("darkMode", String(this.darkMode));
    this.sendData();
  }

  setCurrentTheme(theme){
    this.cookieService.set("currentTheme", JSON.stringify(theme));
    this.currentTheme = theme;
    this.sendData();
  }

  sendData(){
    const send = {
      theme: this.currentTheme,
      darkMode: this.darkMode
    };

    this.comm.emit('changeTheme', send);
  }

}
