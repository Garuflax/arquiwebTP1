import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgmCoreModule } from '@agm/core';

import { LocationRoutingModule } from './location-routing.module';
import { LocationsComponent } from './location-all/location-all.component';
import { LocationDetailComponent } from './location-detail/location-detail.component';



@NgModule({
  declarations: [LocationsComponent, LocationDetailComponent],
  imports: [
    CommonModule,
    LocationRoutingModule,
    AgmCoreModule.forRoot({
      apiKey: ''
    })
  ]
})
export class LocationModule { }

