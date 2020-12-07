import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Title, Meta } from '@angular/platform-browser';
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
    private formBuilder: FormBuilder,
    private titleService: Title,
    private metaTagService: Meta
  ) {
      this.loginForm = this.formBuilder.group({
          username: '',
          password: ''
      });
  }

  ngOnInit(): void {
    this.titleService.setTitle('Login - Yo estuve ahí');
    this.metaTagService.updateTag(
      { name: 'description', content: 'Login Form' }
    );
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