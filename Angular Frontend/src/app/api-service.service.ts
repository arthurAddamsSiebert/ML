import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {

  constructor(private http: HttpClient) {   }
  tmdbApiKey = '1febdcf1ddda86031c084004f3f60295';

  getData() {
    return this.http.get('https://api.binance.com/api/v3/ticker/price');
  }

  sendClicked(data: Array<any>): void{
    
  }

  getRecos(){
    return this.http.get('https://api.binance.com/api/v3/ticker/price');
  }

  getTmdb(id: string){
    return this.http.get('https://api.themoviedb.org/3/movie/'+id+'/images?api_key='+this.tmdbApiKey);
  }

}
