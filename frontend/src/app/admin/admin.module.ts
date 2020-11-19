import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin/admin.component';
import { AuthModule } from './../auth/auth.module';
import { LocationModule } from './../location/location.module';
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';



import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';




@NgModule({
  declarations: [AdminComponent, AdminDashboardComponent],
  imports: [
    CommonModule,
    AdminRoutingModule,
    LocationModule,
    AuthModule,
    MatCardModule,
    FlexLayoutModule
  ]
})
export class AdminModule { }
