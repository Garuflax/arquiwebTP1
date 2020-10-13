import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { LogInForm } from './logInForm';
import { LogInResponse } from './logInResponse';
import { LogOutResponse } from './logOutResponse';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    private authUrl = 'http://127.0.0.1:5000/auth';  // URL to web api

    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient) { }

    /** POST login to the server */
    login(form: LogInForm): Observable<LogInResponse> {
        const url = `${this.authUrl}/login`;
        return this.http.post<LogInResponse>(url, form, this.httpOptions)
        .pipe(
            catchError(this.handleError<LogInResponse>('login'))
            );
    }

    /** logout from the server */
    logout(): Observable<LogOutResponse> {
        const url = `${this.authUrl}/logout:5000`;
        return this.http.get<LogOutResponse>(url)
        .pipe(
            catchError(this.handleError<LogOutResponse>('logout'))
            );
    }

    /**
    * Handle Http operation that failed.
    * Let the app continue.
    * @param operation - name of the operation that failed
    * @param result - optional value to return as the observable result
    */
    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {

            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead

            // TODO: better job of transforming error for user consumption
            console.log(operation);

            // Let the app keep running by returning an empty result.
            return of(result as T);
        };
    }
}
