import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LocationRoutingModule } from './location-routing.module';
import { LocationsComponent } from './location-all/location-all.component';
import { LocationDetailComponent } from './location-detail/location-detail.component';



@NgModule({
  declarations: [LocationsComponent, LocationDetailComponent],
  imports: [
    CommonModule,
    LocationRoutingModule,
  ]
})
export class LocationModule { }

