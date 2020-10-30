import { Component, OnInit } from '@angular/core';
import { AgmCoreModule } from '@agm/core';


@Component({
  selector: 'app-locations',
  templateUrl: './location-all.component.html',
  styleUrls: ['./location-all.component.css']
})
export class LocationsComponent implements OnInit {

  lat: number = 51.678418;
  lng: number = 7.809007;

  constructor() { }

  ngOnInit(): void {
  }

}
