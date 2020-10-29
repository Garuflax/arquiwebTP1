import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

// import { JwtModule } from "@auth0/angular-jwt";
import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";
// Interceptors
import { AuthInterceptorService } from './auth/auth-interceptor.service';
// File Saver
import { FileSaverModule } from 'ngx-filesaver';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthModule } from './auth/auth.module';
import { AdminModule } from './admin/admin.module';
import { UserModule } from './user/user.module';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';


export function tokenGetter() {
  return localStorage.getItem("access_token");
}


@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent,
  ],
  imports: [
    BrowserModule,
    AuthModule,
    AdminModule,
    UserModule,
    AppRoutingModule,
    HttpClientModule,
    // JwtModule.forRoot({
    //   config:{
    //     throwNoTokenError: true,
    //     tokenGetter,
    //     allowedDomains: ['http://localhost:5000'],
    //   }
    // }),
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
