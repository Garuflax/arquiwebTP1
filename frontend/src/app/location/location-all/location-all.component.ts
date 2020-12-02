import { Component, OnInit } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import Map from 'ol/Map';
import View from 'ol/View';
import Feature from 'ol/Feature';
import Overlay from 'ol/Overlay';
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

  constructor(private locationsService: LocationsService) { }

  formatLandmark(id: number, name: string, maximum_capacity: number, people_inside: number) {
    return ('<h2 routerLink="/location/detail/' + id + '">' + name + '</h2>' +
            '<h3>' + people_inside + '/' + maximum_capacity + '</h3>');
  }

  createLandmark(location) {
    let landmarkFeature = new Feature({
      geometry: new Point([location.latitude, location.longitude]),
      location_id: location.id,
      name: location.name,
      maximum_capacity: location.maximum_capacity,
      people_inside: location.people_inside,
    });

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
    /*let popup = new Overlay({
      element: document.getElementById('popup'),
      positioning: 'bottom-center',
      stopEvent: false,
      offset: [0, -50],
    });
    map.addOverlay(popup);
    map.on('click', function (event) {
      var feature = map.getFeaturesAtPixel(event.pixel)[0];
      if (feature) {
        var coordinate = feature.getGeometry().getCoordinates();
        popup.setPosition(coordinate);
        $(element).popover({
          container: element.parentElement,
          html: true,
          sanitize: false,
          content: this.formatLandmark(coordinate, feature.get('location_id'), feature.get('name'), feature.get('maximum_capacity'), feature.get('people_inside')),
          placement: 'top',
        });
        $(element).popover('show');
      } else {
        $(element).popover('dispose');
      }
    });*/

    map.on('pointermove', function (event) {
      if (map.hasFeatureAtPixel(event.pixel)) {
        map.getViewport().style.cursor = 'pointer';
      } else {
        map.getViewport().style.cursor = 'inherit';
      }
    });
  }

  ngOnInit(): void {
    useGeographic();
    this.locationsService.get_locations()
      .subscribe( 
        (data) => {
          this.createMap('locations_map', [-58.4323658, -34.5655463], data["locations"]);
        }
    )
  }

}
