import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-step2',
  templateUrl: './step2.component.html',
  styleUrls: ['./step2.component.scss']
})
export class Step2Component implements OnInit {

  constructor(private api: ApiServiceService) { }
  rocs: Object;
  clickedTitles: Array<string> = [];
  ngOnInit(): void {
    this.api.getRecos().subscribe(data => {
      this.rocs = data;
      console.log(this.rocs);
    });
  }

}
