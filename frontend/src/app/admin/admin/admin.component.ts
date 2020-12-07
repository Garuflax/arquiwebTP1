import { Component, OnInit } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';
import { AdminDashboardComponent } from './../admin-dashboard/admin-dashboard.component'

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})

export class AdminComponent implements OnInit {

  constructor(
        private titleService: Title,
        private metaTagService: Meta
    ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Menú de administrador - Yo estuve ahí');
    this.metaTagService.updateTag(
      { name: 'description', content: 'Estadísticas de usuarios' }
    );
  }

}
