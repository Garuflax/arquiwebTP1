import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class AdminService {

  private locationsDataUrl = 'http://127.0.0.1:5000/admin/locations';
  private usersDataUrl = 'http://127.0.0.1:5000/admin/users';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json'})
  };

  constructor(private http: HttpClient) { }

  get_locations_data() {
    return this.http.get(this.locationsDataUrl)
  }

  get_users_data() {
    return this.http.get(this.usersDataUrl)
  }
}
