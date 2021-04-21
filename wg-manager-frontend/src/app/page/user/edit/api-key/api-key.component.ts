import {Component, OnInit} from '@angular/core';
import {ServerService} from "../../../../services/server.service";

@Component({
  selector: 'app-api-key',
  templateUrl: './api-key.component.html',
  styleUrls: ['./api-key.component.scss']
})
export class ApiKeyComponent implements OnInit {

  displayedColumns: string[] = ['id', 'key', 'created_at', 'delete'];
  dataSource = [];

  constructor(private serverService: ServerService
  ) { }

  ngOnInit(): void {


    this.serverService.getAPIKeys().subscribe((apiKeys: Array<any>) => {
      this.dataSource = [...apiKeys]

      console.log(this.dataSource)
    })
  }

  deleteAPIKey(elem){
    let idx = this.dataSource.indexOf(elem);
    this.serverService.deleteAPIKey(elem.id).subscribe(x => {
      this.dataSource.splice(idx, 1);
      this.dataSource = [...this.dataSource]
    })
  }

  createAPIKey(){

    this.serverService.addAPIKey().subscribe(key => {
      this.dataSource.push(key)
      this.dataSource = [...this.dataSource]

    })

  }

}
