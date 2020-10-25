import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { FormBuilder } from '@angular/forms';
import { AuthService } from '../auth.service';
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
            if(response.is_admin){
                this.router.navigate(['/admin']);
            } else {
                this.router.navigate(['/user']);
            }});

        this.loginForm.reset();
    }

    register(userData) {
        this.authService.register(userData)
        .subscribe(response => console.log(response));//TODO redirect
        
        this.registerForm.reset();

        console.log('Registered successfully?', userData);
    }

}
