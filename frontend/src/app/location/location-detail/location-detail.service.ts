import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';;

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class LocationDetailService {

  constructor(private http: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  get_qr(location_id: Number) {
    const url = `http://127.0.0.1:5000/location/${location_id}/qrcode`;
    return this.http.get(url, {responseType: 'blob'}) 
}
}
