import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgmCoreModule } from '@agm/core';

import { LocationRoutingModule } from './location-routing.module';
import { LocationsComponent } from './location-all/location-all.component';
import { LocationDetailComponent } from './location-detail/location-detail.component';

import { MatFormFieldModule } from '@angular/material/form-field'; 
import { MatInputModule } from '@angular/material/input'; 
import { MatButtonModule } from '@angular/material/button' 
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
  declarations: [LocationsComponent, LocationDetailComponent],
  imports: [
    CommonModule,
    LocationRoutingModule,
    AgmCoreModule.forRoot({
      apiKey: ''
    }),
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    FlexLayoutModule,
    MatToolbarModule,
    MatIconModule
  ],
  exports: [LocationsComponent, LocationDetailComponent]
})
export class LocationModule { }

