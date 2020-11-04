import { Component, OnInit } from '@angular/core';
import { AdminService } from './../admin.service'

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})

export class AdminDashboardComponent implements OnInit {

  locations_data;
  users_data;

  constructor(private adminService: AdminService) { }

  ngOnInit(): void {

    

    this.adminService.get_locations_data()
      .subscribe( 
        (data) => {this.locations_data = data;}
    )

    this.adminService.get_users_data()
      .subscribe( 
        (data) => {this.users_data = data;}
    )

  }

}
