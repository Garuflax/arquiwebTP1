import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegistrationComponent } from './auth/registration/registration.component';

import { PageNotFoundComponent } from './page-not-found/page-not-found.component';


const routes: Routes = [
    { path: '', redirectTo: '/auth', pathMatch: 'full' },
    // { path: 'log', component: LoginComponent },
    // { path: 'reg', component: RegistrationComponent },
    { path: 'auth', loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule) },
    { path: 'admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
    { path: 'user', loadChildren: () => import('./user/user.module').then(m => m.UserModule) },
    { path: 'location', loadChildren: () => import('./location/location.module').then(m => m.LocationModule) },
    { path: '**', component: PageNotFoundComponent }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})

export class AppRoutingModule { }