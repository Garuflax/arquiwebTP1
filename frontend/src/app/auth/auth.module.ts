import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';

import { AuthRoutingModule } from './auth-routing.module';
import { LogOutComponent } from './log-out/log-out.component';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';

import { MatFormFieldModule } from '@angular/material/form-field'; 
import { MatInputModule } from '@angular/material/input'; 
import { MatButtonModule } from '@angular/material/button' 
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';

@NgModule({
  declarations: [
    LogOutComponent,
    LoginComponent,
    RegistrationComponent
  ],
  imports: [
    CommonModule,
    AuthRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    FlexLayoutModule,
    MatInputModule,
    MatButtonModule ,
    MatCardModule,
    MatToolbarModule,
    MatIconModule
  ],
  exports: [LogOutComponent]
})
export class AuthModule { }
