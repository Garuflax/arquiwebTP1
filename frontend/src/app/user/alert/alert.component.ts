import { Component, OnInit } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.css']
})
export class AlertComponent implements OnInit {

  constructor(
        private titleService: Title,
        private metaTagService: Meta
      ) { }

  ngOnInit(): void {
      this.titleService.setTitle('Alerta - Yo estuve ahí');
      this.metaTagService.updateTag(
        { name: 'description', content: 'Informarse que está en riesgo de contagio' }
      );
  }

}
