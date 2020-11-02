import { Component, OnInit } from '@angular/core';
import { CheckService } from './../check/check.service'

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  has_to_checkin;
  a;

  constructor(private checkService: CheckService) { }

  ngOnInit(): void {
    this.checkService.currentLocation()
      .subscribe( 
        (location) => {
          this.has_to_checkin = location["current_location"] == null;
        }
    )
  }

  inform(): void {
      //TODO: send to the server the change of state that applies
  }

}
