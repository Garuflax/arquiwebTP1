import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserComponent } from './user/user.component';
import { LocationManagerComponent } from './location-manager/location-manager.component';
import { CheckComponent } from './check/check.component';


const routes: Routes = [
    { path: '', component: UserComponent },
    { path: 'manage', component: LocationManagerComponent },
    { path: 'checkin', component: CheckComponent },
    { path: 'checkout', component: CheckComponent },


];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
