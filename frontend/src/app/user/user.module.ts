import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';

import { UserRoutingModule } from './user-routing.module';
import { UserComponent } from './user/user.component';
import { CheckComponent } from './check/check.component';

import { ZXingScannerModule } from '@zxing/ngx-scanner';
import { LocationManagerComponent } from './location-manager/location-manager.component';
import { AlertComponent } from './alert/alert.component';
import { AuthModule } from './../auth/auth.module';
import { AdminModule } from '../admin/admin.module';
import { AdminComponent } from '../admin/admin/admin.component';
import { AdminDashboardComponent } from '../admin/admin-dashboard/admin-dashboard.component';
import { LocationModule } from '../location/location.module'

// Flex
import { FlexLayoutModule } from '@angular/flex-layout';

// Angular Material Stuff

import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';  
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card'; 

import { MatToolbarModule } from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';

@NgModule({
  declarations: [UserComponent, CheckComponent, LocationManagerComponent, AlertComponent],
  imports: [
    CommonModule,
    UserRoutingModule,
    ZXingScannerModule,
    FormsModule,
    ReactiveFormsModule,
    AuthModule,
    LocationModule,
    // Angular Stuff
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatCardModule,
    FlexLayoutModule,
    MatToolbarModule,
    MatIconModule
  ]
})
export class UserModule { }
