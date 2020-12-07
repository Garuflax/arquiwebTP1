import { Component } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Meta } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Yo estuve ahí';
  subtitle = 'COVID tracker';

  constructor(
      public http: HttpClient,
      private metaTagService: Meta
    ) {}

  ngOnInit() {
      this.metaTagService.addTags([
          { name: 'keywords', content: 'Angular' },
          { name: 'author', content: 'Facundo Linari, Francisco Castagna' },
          { name: 'date', content: '2020-12-09', scheme: 'YYYY-MM-DD' }
      ]);
  }

   
}
