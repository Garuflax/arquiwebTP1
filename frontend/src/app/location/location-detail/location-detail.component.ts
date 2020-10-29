import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { LocationsService } from './../location-all/location-all.service';


@Component({
  selector: 'app-location-detail',
  templateUrl: './location-detail.component.html',
  styleUrls: ['./location-detail.component.css']
})
export class LocationDetailComponent implements OnInit {

  public location_id: number;
  public maximum_capacity: number;
  public people_inside: number;
  public author_id: number;
  public name: string;

  constructor(
    private locationsService: LocationsService,
    private router: Router,
    private route: ActivatedRoute,
  ){}

  ngOnInit(): void {
    this.location_id = Number(this.route.snapshot.paramMap.get('id'));
    this.locationsService.get_location(this.location_id)
      .subscribe( 
        (location_state) => {
          this.maximum_capacity = location_state['maximum_capacity']
          this.people_inside = location_state['people_inside']
          this.name = location_state['name']
          this.author_id = location_state['author_id']
        }
      )
  }

  onDownloadQr() {
    // this.checkService.get_qr(this.location_id)
    // .subscribe()
  }

}
