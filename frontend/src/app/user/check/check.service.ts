import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class CheckService {

  private checkinUrl = 'https://yeacovid.herokuapp.com/checkin';
  private checkoutUrl = 'https://yeacovid.herokuapp.com/checkout';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) {}

  /** POST checkin to the server */
  checkin(qr_result: Number) {
    return this.http.post(this.checkinUrl, {location_id:qr_result}, this.httpOptions)
  }

  /** POST checkout to the server */
  checkout(qr_result: Number) {
    return this.http.post(this.checkoutUrl, {location_id:qr_result}, this.httpOptions)
  }

}
