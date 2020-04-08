import { Component, HostBinding } from '@angular/core';


@Component({
  selector: 'app-components',
  templateUrl: './components.component.html',
  styleUrls: ['./components.component.scss'],
})
export class ComponentsComponent {
  @HostBinding('class.mdl-grid') private readonly mdlGrid = true;
  @HostBinding('class.ui-components') private readonly uiComponents = true;

  public data = [
    {
      name: 'Nathan Fillion',
      description: 'Malcolm “Mal” Reynolds',
      image: 'nathan-fillion.png',
    },
    {
      name: 'Gina Torres',
      description: 'Zoe Alleyne Washburne',
      image: 'gina-torres.png',
    },
    {
      name: 'Alan Tudyk',
      description: 'Hoban “Wash” Washburne',
      image: 'tudyk.png',
    },
  ];
}
