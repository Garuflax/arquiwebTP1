import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LocationDetailComponent } from './location-detail/location-detail.component';
import { LocationsComponent } from './location-all/location-all.component';


const routes: Routes = [
    { path: 'all', component: LocationsComponent },
    { path: ':id', component: LocationDetailComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LocationRoutingModule { }

