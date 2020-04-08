import { Component, OnInit } from '@angular/core';
import {Observable} from "rxjs";
import {BreakpointObserver, Breakpoints} from "@angular/cdk/layout";
import {map, shareReplay} from "rxjs/operators";
import {ConfigService} from "../../services/config.service";

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  menu: Array<{link: Array<string>, icon: string, text: string}> = [
    { link: ["/page/dashboard"], icon: "home", text: "Dashboard"}
  ];

  constructor(private breakpointObserver: BreakpointObserver, public config: ConfigService) {}
  ngOnInit(): void {
    console.log("Layout")
  }

}
