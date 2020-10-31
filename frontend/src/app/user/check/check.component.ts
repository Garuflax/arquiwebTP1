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

  qrResult: string;

  constructor(
    private checkService: CheckService,
    private router: Router,
  ){}

  ngOnInit(): void {
    // ver si el usuario hizo checkin
  }

  // QR scanner stuff

  onCodeResult(result: string) {

    this.qrResult = result
    // Si el usuario aún no hizo checkin
    this.checkService.checkin(this.qrResult)
      .subscribe( 
        () => this.router.navigate(['/locations/detail', Number(result)])
    )
    // Si el usuario ya hizo checkin, hace checkout. Vuelve a user
    this.checkService.checkout(this.qrResult)
      .subscribe( 
        () => this.router.navigate(['/user'])
    )
      }

  // Ver si lo puedo quitar
  toggleTryHarder(): void {
    this.tryHarder = !this.tryHarder;
  }

}
