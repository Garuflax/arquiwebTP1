import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
    selector: 'app-log-out',
    templateUrl: './log-out.component.html',
    styleUrls: ['./log-out.component.css']
})
export class LogOutComponent implements OnInit {

    constructor(
        private router: Router,
        private authService: AuthService
        ) { }

    ngOnInit(): void {
    }

    logout() {
        this.authService.logout()
        .subscribe(response => {
            localStorage.removeItem('accessToken');
            this.router.navigate(['/auth']);
        });
    }

}
