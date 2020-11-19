import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { GetStatusService } from 'src/app/user/get-status.service';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
  registerForm;
  constructor(
    private router: Router,
    private authService: AuthService,
    private getStatusService: GetStatusService,
    private formBuilder: FormBuilder
    ) {
    this.registerForm = this.formBuilder.group({
        username: '',
        password: '',
        email: ''
    });
  }

  ngOnInit(): void {
  }

  register(userData) {
    this.authService.register(userData)
    .subscribe(response => console.log(response));

    this.registerForm.reset();

    console.log('Registered successfully?', userData);
  }



}
