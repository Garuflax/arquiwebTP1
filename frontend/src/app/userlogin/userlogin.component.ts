import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-userlogin',
  templateUrl: './userlogin.component.html',
  styleUrls: ['./userlogin.component.css'],
})
export class UserloginComponent   {
  nombreIngresado = '';
  onEnter(value: string) { this.nombreIngresado = value; }

}
