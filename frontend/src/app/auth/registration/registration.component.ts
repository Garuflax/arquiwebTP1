import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { Title, Meta } from '@angular/platform-browser';
import { GetStatusService } from 'src/app/user/get-status.service';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
  registerForm;
  message: string;
  constructor(
    private router: Router,
    private authService: AuthService,
    private getStatusService: GetStatusService,
    private formBuilder: FormBuilder,
    private titleService: Title,
    private metaTagService: Meta
    ) {
    this.registerForm = this.formBuilder.group({
        username: '',
        password: '',
        email: ''
    });
  }

  ngOnInit(): void {
    this.titleService.setTitle('Registro - Yo estuve ahí');
    this.metaTagService.updateTag(
      { name: 'description', content: 'Formulario de Registro' }
    );
  }

  register(userData) {
    this.authService.register(userData)
    .subscribe(response => {
      this.message = response["message"];
      if (response.created) {
        setTimeout( () => this.router.navigate(['/auth']), 5000);
      }
      });

    this.registerForm.reset();
  }



}
