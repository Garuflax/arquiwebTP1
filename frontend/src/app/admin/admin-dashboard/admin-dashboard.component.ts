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
  number_of_infected;
  number_of_locations;
  number_of_users;

  constructor(private adminService: AdminService) { }

  ngOnInit(): void {

    

    this.adminService.get_locations_data()
      .subscribe( 
        (data) => {
          this.locations_data = data;
          this.number_of_locations = data["locations"].length;
        }
    )

    this.adminService.get_users_data()
      .subscribe( 
        (data) => {
          this.users_data = data;
          this.number_of_users = Object.keys(data).length;
          // this.number_of_infected = 0;
          this.number_of_infected = Object.keys(data).filter(user => data[user]["is_infected"]).length
          // for (var i=0; i<Object.keys(data).length; i++){
          //   if (data[i]["is_infected"]){
          //     this.number_of_infected ++;
          //   }
          // }
        }
    )

  }

}
