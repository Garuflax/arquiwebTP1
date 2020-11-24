import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';;

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class LocationsService {

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) { }

  /** GET location to the server */
  get_location(id : Number) {
    return this.http.get(`https://yeacovid/location/${id}`)
  }

  get_locations() {
    return this.http.get("https://yeacovid/location/all")
  }

}