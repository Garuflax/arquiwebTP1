import { Component, OnInit } from '@angular/core';
import { CheckService } from './check.service'
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.css']
})
export class CheckComponent implements OnInit {

  currentDevice: MediaDeviceInfo = null;
  tryHarder = false;
  has_to_checkin;

  qrResult: string;

  constructor(
    private checkService: CheckService,
    private router: Router,
  ){}

  ngOnInit(): void {
    this.has_to_checkin = this.router.url == "/user/checkin";
  }


  onCodeResult(result: string) {

    this.qrResult = result

    // Si el usuario no hizo checkin, hace checkin. Va a location/detail/resultQR
    if (this.has_to_checkin){
      this.checkService.checkin(this.qrResult)
      .subscribe( 
        () => this.router.navigate(['/location/detail', Number(result)])
    )
    }
    // Si el usuario ya hizo checkin, hace checkout. Vuelve a user
    else{
      this.checkService.checkout(this.qrResult)
      .subscribe( 
        () => this.router.navigate(['/user'])
    )
    }
      }

  // Ver si lo puedo quitar
  toggleTryHarder(): void {
    this.tryHarder = !this.tryHarder;
  }

}
