import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { Title, Meta } from '@angular/platform-browser';
import { FormBuilder } from '@angular/forms';
import { AddLocationService } from '../../location/add-location.service';

@Component({
  selector: 'app-location-manager',
  templateUrl: './location-manager.component.html',
  styleUrls: ['./location-manager.component.css']
})
export class LocationManagerComponent implements OnInit {

  locationForm;

  constructor(
        private router: Router,
        private addLocationService: AddLocationService,
        private formBuilder: FormBuilder,
        private titleService: Title,
        private metaTagService: Meta
        ) {
      this.locationForm = this.formBuilder.group({
            name: '',
            maximum_capacity: '',
            latitude: '',
            longitude: ''
        });
  }

  ngOnInit(): void {
    this.titleService.setTitle('Menú de locación - Yo estuve ahí');
    this.metaTagService.updateTag(
      { name: 'description', content: 'Agregar y mirar locaciones' }
    );
  }

  onSuggestion($event) {
    let lat = $event.suggestion.latlng.lat
    let lng = $event.suggestion.latlng.lng
    let name = $event.suggestion.name
    this.locationForm.get('latitude').setValue(lng)
    this.locationForm.get('longitude').setValue(lat)
    this.locationForm.get('name').setValue(name)
  }

  addLocation(locationData) {
      this.addLocationService.addLocation(locationData)
        .subscribe(response => {
            this.router.navigate(['/user']);
            });

        this.locationForm.reset();
  }


}
