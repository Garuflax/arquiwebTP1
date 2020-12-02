import { Component, OnInit } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import Map from 'ol/Map';
import View from 'ol/View';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style';
import Icon from 'ol/style/Icon';
import OSM from 'ol/source/OSM';
import * as olProj from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import {useGeographic} from 'ol/proj';

import { LocationsService } from './location-all.service';



@Component({
  selector: 'app-locations',
  templateUrl: './location-all.component.html',
  styleUrls: ['./location-all.component.css']
})
export class LocationsComponent implements OnInit {

  map;

  constructor(private locationsService: LocationsService) { }

  createLandmark(location) {
    console.log(location);
    let landmarkFeature = new Feature({
      geometry: new Point([location.latitude, location.longitude]),
      name: location.name,
      /*id: location.id,
      maximum_capacity: location.maximum_capacity,
      people_inside: location.people_inside,*/
    });

    // let landmarkStyle = new Style({
    //   image: new Icon({
    //     anchor: [0.5, 46],
    //     anchorXUnits: 'fraction',
    //     anchorYUnits: 'pixels',
    //     src: 'data/icon.png',
    //   }),
    // });

    // landmarkFeature.setStyle(landmarkStyle);
    return landmarkFeature;
  }

  createMap(id: string, viewCenter: [number, number], locations) {
    var vectorSource = new VectorSource({
      features: locations.map(this.createLandmark)
    });

    let map = new Map({
      target: id,
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        new VectorLayer({
          source: vectorSource,
          /*style: new Style({
            fill: new Fill({
              color: 'rgba(255, 255, 255, 0.2)',
            }),
            stroke: new Stroke({
              color: '#ffcc33',
              width: 2,
            }),
            image: new CircleStyle({
              radius: 7,
              fill: new Fill({
                color: '#ffcc33',
              }),
            }),
          })*/
        })
      ],
      view: new View({
        center: viewCenter,
        zoom: 5
      })
    });
  }

  ngOnInit(): void {
    useGeographic();
    this.locationsService.get_locations()
      .subscribe( 
        (data) => {
          this.map = this.createMap('locations_map', [-58.4323658, -34.5655463], data["locations"]);
        }
    )
  }

}
