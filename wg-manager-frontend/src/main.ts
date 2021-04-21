import { enableProdMode, ViewEncapsulation } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app';
import { environment } from './environments/environment';
import 'hammerjs';

(function () {
  if (typeof EventTarget !== 'undefined') {
    const func = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function (type, fn, capture) {
      this.func = func;
      if (typeof capture !== 'boolean') {
        capture = capture || {};
        capture.passive = false;
      }
      this.func(type, fn, capture);
    };
  }
}());
if (environment.production) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(AppModule, { defaultEncapsulation: ViewEncapsulation.None });
