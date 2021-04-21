import {Component, HostBinding} from '@angular/core';
import { AuthService } from '@services/*';
import {OverlayContainer} from "@angular/cdk/overlay";
import {DataService} from "./services/data.service";
import {CookieService} from "ngx-cookie-service";

const THEME_DARKNESS_SUFFIX = `-dark`;

@Component({
  selector: 'app-root',
  template: `<router-outlet></router-outlet>`,
})
export class AppComponent {
  @HostBinding('class') activeThemeCssClass: string;
  isThemeDark = false;
  activeTheme: string;

  constructor(
    private auth:
      AuthService,
    private overlayContainer: OverlayContainer,
    private comm: DataService,
    private cookieService: CookieService
  ) {
    auth.init();

    this.comm.on("changeTheme").subscribe( (data: {
      theme: any,
      darkMode: boolean
    }) => {
      this.setActiveTheme(data.theme.theme, /* darkness: */ data.darkMode)
    });

    if(this.cookieService.check("currentTheme")){
      this.setActiveTheme(
        JSON.parse(this.cookieService.get("currentTheme")).theme,
        (this.cookieService.get("darkMode") === 'true')
      );

    }





  }

  setActiveTheme(theme: string, darkness: boolean = null) {
    if (darkness === null)
      darkness = this.isThemeDark;
    else if (this.isThemeDark === darkness) {
      if (this.activeTheme === theme) return
    } else
      this.isThemeDark = darkness;

    this.activeTheme = theme;

    const cssClass = darkness === true ? theme + THEME_DARKNESS_SUFFIX : theme;

    const classList = this.overlayContainer.getContainerElement().classList;
    if (classList.contains(this.activeThemeCssClass))
      classList.replace(this.activeThemeCssClass, cssClass);
    else
      classList.add(cssClass);

    this.activeThemeCssClass = cssClass
  }
}
