import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { User } from '../user';
import { LogInForm } from '../logInForm';

@Component({
  selector: 'app-userlogin',
  templateUrl: './userlogin.component.html',
  styleUrls: ['./userlogin.component.css'],
})
export class UserloginComponent   {
  user

  constructor(private authService: AuthService) { }

  onEnter(nameValue: string, passValue: string) {
    this.user = new User(nameValue, passValue);
    const form: LogInForm = {
        username  : nameValue,
        password  : passValue
    };
    this.authService.login(form)
    .subscribe(response => console.log(response));//TODO redirect
    }

}
