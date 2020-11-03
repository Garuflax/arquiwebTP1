import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class InformService {

  private informUrl = 'http://127.0.0.1:5000/inform';  // URL to web api

  httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) { }

  /** POST infection to the server */
  infection(date) {
      const url = `${this.informUrl}/infection`;
      return this.http.post(url, date, this.httpOptions);
  }

  /** POST discharge to the server */
  discharge(date) {
      const url = `${this.informUrl}/discharge`;
      return this.http.post(url, date, this.httpOptions);
  }
}
