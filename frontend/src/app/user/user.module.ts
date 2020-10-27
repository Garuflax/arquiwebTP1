import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { UserComponent } from './user/user.component';
import { LocationsComponent } from './locations/locations.component';
import { CheckComponent } from './check/check.component';

import { ZXingScannerModule } from '@zxing/ngx-scanner';
import { LocationDetailComponent } from './locations/location-detail.component';


@NgModule({
  declarations: [UserComponent, LocationsComponent, CheckComponent, LocationDetailComponent],
  imports: [
    CommonModule,
    UserRoutingModule,
    ZXingScannerModule
  ]
})
export class UserModule { }
