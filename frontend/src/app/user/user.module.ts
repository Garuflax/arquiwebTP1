import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { UserComponent } from './user/user.component';
import { CheckComponent } from './check/check.component';

import { ZXingScannerModule } from '@zxing/ngx-scanner';


@NgModule({
  declarations: [UserComponent, CheckComponent],
  imports: [
    CommonModule,
    UserRoutingModule,
    ZXingScannerModule
  ]
})
export class UserModule { }
