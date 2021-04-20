import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../api-service.service';

import { from } from 'rxjs';
@Component({
  selector: 'app-step1',
  templateUrl: './step1.component.html',
  styleUrls: ['./step1.component.scss']
})
export class Step1Component implements OnInit {

  constructor(private api: ApiServiceService) { }
  angabenMachen = true;
  step1 = true;
  step2 = false;
  titles: any = [];
  newTitles: any = [];
  clickedTitles: Array<string> = [];
  apiClicked: Object;
  currentMovieIdData: Object;
  imgArray: Array<string> = ['eKtuGJQJ06iafhYl22mYCWidjmM.jpg'];
  ngOnInit(): void {
    this.init();

  }

  async init(){
    this.titles = await this.api.getData()
  }

  async onClick(title: string){
    if(this.angabenMachen==true){
      if(this.clickedTitles.indexOf(title) > -1){
      
        var index = this.clickedTitles.indexOf(title);
        this.clickedTitles.splice(index, 1);
      } else {
        this.clickedTitles.push(title);
      }
      this.api.sendClicked(this.clickedTitles);
    }
    
  }

  async sendReq(){
    if(this.angabenMachen==true){
      if(this.clickedTitles.length > 4){
        this.step1 =false;
        this.step2 = true;
        console.log(this.clickedTitles);
      //this.api.getRecos(this.clickedTitles);
      const res = await this.api.getRecos({ids:this.clickedTitles});
        //for(let)

      console.log(res);
      console.log(res);
      console.log(this.titles.test);
      this.newTitles = { test: res};
      console.log(this.titles);
      console.log(this.titles.test);
      document.getElementById('button').innerHTML = 'Restart';
      this.angabenMachen = false;
      }else{
        alert('Bitte wählen Sie mindestens 5 Titel aus');
      }
    } else {
      window.location.reload();
    }
    
    
  }
  
  getImage(id: string){
    return 'https://www.themoviedb.org/t/p/w1280/'+this.imgArray[0];
  }

}
