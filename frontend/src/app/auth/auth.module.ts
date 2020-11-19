import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';

import { AuthRoutingModule } from './auth-routing.module';
import { MenuComponent } from './menu/menu.component';
import { LogOutComponent } from './log-out/log-out.component';


@NgModule({
  declarations: [
    MenuComponent,
    LogOutComponent
  ],
  imports: [
    CommonModule,
    AuthRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  exports: [LogOutComponent]
})
export class AuthModule { }
