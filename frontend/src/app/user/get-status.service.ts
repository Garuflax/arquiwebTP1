import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { StatusResponse } from './statusResponse';

@Injectable({
  providedIn: 'root'
})
export class GetStatusService {

  private getStatusUrl = 'http://127.0.0.1:5000/status';  // URL to web api

  constructor(private http: HttpClient) { }

  /** GET status from the server */
  getStatus(): Observable<StatusResponse> {
      return this.http.get<StatusResponse>(this.getStatusUrl);
  }
}