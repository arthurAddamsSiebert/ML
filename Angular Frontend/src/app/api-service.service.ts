import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  all: any;

  constructor(private http: HttpClient) {   }
  tmdbApiKey = '1febdcf1ddda86031c084004f3f60295';

  async getData() {
    this.all = await this.http.get('http://localhost:4200/api/all').toPromise()
    return this.all;
  }

  sendClicked(data: Array<any>): void{
    
  }

  async getRecos(body: any){
    try{
      console.log(body);
      const res = await this.http.post('http://localhost:4200/api/getRecommendations', body).toPromise();
      console.log(res);
      console.log(this.all);
      console.log();
      const recos = res['response'].map((e) => e[1]).flat().map((e)=> this.all.test.filter((x)=> x[0] == e)[0]);
      return recos;
    }catch(e){
      console.log(e);
    }
    
  }

  getTmdb(id: string){
    return this.http.get('https://api.themoviedb.org/3/movie/'+id+'/images?api_key='+this.tmdbApiKey);
  }

}
