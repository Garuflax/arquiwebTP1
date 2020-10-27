import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserComponent } from './user/user.component';
import { LocationsComponent } from './locations/locations.component';
import { LocationDetailComponent } from './locations/location-detail.component'
import { CheckComponent } from './check/check.component';


const routes: Routes = [
    { path: '', component: UserComponent },
    { path: 'locations', component: LocationsComponent },
    { path: 'locations/:id', component: LocationDetailComponent },
    { path: 'checkin', component: CheckComponent },
    { path: 'checkout', component: CheckComponent }

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
