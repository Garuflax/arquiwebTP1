import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { UserComponent } from './user/user.component';
import { LocationsComponent } from './locations/locations.component';
import { CheckComponent } from './check/check.component';


@NgModule({
  declarations: [UserComponent, LocationsComponent, CheckComponent],
  imports: [
    CommonModule,
    UserRoutingModule
  ]
})
export class UserModule { }
