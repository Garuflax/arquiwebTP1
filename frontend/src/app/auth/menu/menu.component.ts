import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { FormBuilder } from '@angular/forms';
import { AuthService } from '../auth.service';
import { GetStatusService } from '../../user/get-status.service';
import { LogInForm } from '../logInForm';
import { RegisterForm } from '../registerForm';


@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
    loginForm;
    registerForm;

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
        this.registerForm = this.formBuilder.group({
            username: '',
            password: '',
            email: ''
        });
    }

    ngOnInit(): void {
    }

    login(userData) {
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
            });

        this.loginForm.reset();
    }

    register(userData) {
        this.authService.register(userData)
        .subscribe(response => console.log(response));

        this.registerForm.reset();

        console.log('Registered successfully?', userData);
    }

}
