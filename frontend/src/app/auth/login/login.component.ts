import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { GetStatusService } from 'src/app/user/get-status.service';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm;
  isLoginFailed = false;
  errorMessage = '';

  constructor(
    private router: Router,
    private authService: AuthService,
    private getStatusService: GetStatusService,
    private formBuilder: FormBuilder
  ) {
      this.loginForm = this.formBuilder.group({
          username: '',
          password: ''
      });
  }

  ngOnInit(): void {
  }

  login(userData) {
    this.isLoginFailed = false;
    this.authService.login(userData)
    .subscribe(response => {
        localStorage.setItem('accessToken', response.access_token);

        this.getStatusService.getStatus().subscribe(response => {
            if(response.is_admin){
                this.router.navigate(['/admin']);
            } else if(response.being_in_risk_since){
                this.router.navigate(['/user/alert']);
            } else {
                this.router.navigate(['/user']);
            }
            });
        }, err => {
          this.isLoginFailed = true;
          this.errorMessage = err.error.message + " " + err.error.error;
        }
        );

    this.loginForm.reset();
}

}