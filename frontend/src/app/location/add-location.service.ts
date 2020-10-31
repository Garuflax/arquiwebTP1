import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { LocationForm } from './locationForm';

@Injectable({
  providedIn: 'root'
})
export class AddLocationService {

  private locationCreateUrl = 'http://127.0.0.1:5000/location/create';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) { }

  /** POST location/create to the server */
  addLocation(form: LocationForm) {
      return this.http.post(this.locationCreateUrl, form, this.httpOptions);
  }
}
