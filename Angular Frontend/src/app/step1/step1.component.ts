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
  titles: any = [];
  newTitles: any = [];
  clickedTitles: Array<string> = [];
  apiClicked: Object;
  currentMovieIdData: Object;
  imgArray: Array<string> = ['eKtuGJQJ06iafhYl22mYCWidjmM.jpg'];
  ngOnInit(): void {
    this.api.getData().subscribe(data => {
      this.titles = data;
      console.log(this.titles);
    });

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
        console.log(this.clickedTitles);
      this.api.sendClicked(this.clickedTitles);
      let entry: any;
      var count = 0;
      for(let entry of this.titles){
        count++;
      }
      for(let i = 0;i < count;i++){
        if(this.clickedTitles.indexOf(this.titles[i].symbol) > -1){
          this.newTitles.push(this.titles[i]);
        }
      }
      this.titles = this.newTitles;
      document.getElementById('button').innerHTML = 'Restart';
      this.angabenMachen = false;
      }else{
        alert('Bitte wählen mindestens 5 Titel aus');
      }
    } else {
      window.location.reload();
    }
    
    
  }
  
  getImage(id: string){
    return 'https://www.themoviedb.org/t/p/w1280/'+this.imgArray[0];
  }

}
