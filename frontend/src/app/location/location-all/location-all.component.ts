import { Component, OnInit } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import { LocationsService } from './location-all.service'

@Component({
  selector: 'app-locations',
  templateUrl: './location-all.component.html',
  styleUrls: ['./location-all.component.css']
})
export class LocationsComponent implements OnInit {

  lat: number = 30.678418;
  lng: number = 60.809007;
  locations;

  constructor(private locationsService: LocationsService) { }

  ngOnInit(): void {
    this.locationsService.get_locations()
      .subscribe( 
        (data) => {
          this.locations = data["locations"];
        }
    )
  }

}
