import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-userlogin',
  templateUrl: './userlogin.component.html',
  styleUrls: ['./userlogin.component.css'],
})
export class UserloginComponent   {
  nombreIngresado = '';
  passwordIngresado = '';
  onEnter(nameValue: string, passValue: string) { this.nombreIngresado = nameValue; this.passwordIngresado=passValue;  }

}
