import { Component, OnInit } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';
import { GetStatusService } from '../get-status.service'
import { InformService } from '../inform.service'

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  has_to_checkin;
  is_infected;

  constructor(private getStatusService: GetStatusService,
    private informService: InformService,
    private titleService: Title,
    private metaTagService: Meta
    ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Menú de usuario - Yo estuve ahí');
    this.metaTagService.updateTag(
      { name: 'description', content: 'User Menu' }
    );
    this.getStatusService.getStatus()
      .subscribe( 
        (response) => {
          this.has_to_checkin = response["current_location"] == null;
          this.is_infected = response["is_infected"];
        }
    )
  }

  informInfection(): void {
      this.informService.infection({date: 1}).subscribe(response => this.is_infected = true); // TODO: get date
  }

  informDischarge(): void {
      this.informService.discharge({date: 1}).subscribe(response => this.is_infected = false); // TODO: get date
  }

}
