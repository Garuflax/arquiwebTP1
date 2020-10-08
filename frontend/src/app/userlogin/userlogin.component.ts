import { Component, OnInit } from '@angular/core';
import { User } from '../user';

@Component({
  selector: 'app-userlogin',
  templateUrl: './userlogin.component.html',
  styleUrls: ['./userlogin.component.css'],
})
export class UserloginComponent   {
  user

  onEnter(nameValue: string, passValue: string) {
    this.user = new User(nameValue, passValue)
    }

}
