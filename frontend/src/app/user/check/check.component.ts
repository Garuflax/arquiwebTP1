import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';
import { CheckService } from './check.service'
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { QrScannerComponent } from 'angular2-qrscanner';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class CheckComponent implements OnInit {

  currentDevice: MediaDeviceInfo = null;
  tryHarder: boolean = true;
  has_to_checkin: boolean;
  message: string;
  scanned: boolean = false;

  qrResult: string;

  constructor(
    private checkService: CheckService,
    private router: Router,
    private titleService: Title,
    private metaTagService: Meta
  ){}

  // @ViewChild('test', {static: true}) test;
  
  @ViewChild(QrScannerComponent, {static: true}) qrScannerComponent ;
  ngOnInit(): void {
    this.titleService.setTitle('Check - Yo estuve ahí');
    this.metaTagService.updateTag(
      { name: 'description', content: 'Entrar o salir de locación' }
    );
    this.has_to_checkin = this.router.url == "/user/checkin";


    this.qrScannerComponent.getMediaDevices().then(devices => {
      const videoDevices: MediaDeviceInfo[] = [];
      for (const device of devices) {
          if (device.kind.toString() === 'videoinput') {
              videoDevices.push(device);
          }
      }
      if (videoDevices.length > 0){
          let choosenDev;
          for (const dev of videoDevices){
              if (dev.label.includes('front')){
                  choosenDev = dev;
                  break;
              }
          }
          if (choosenDev) {
              this.qrScannerComponent.chooseCamera.next(choosenDev);
          } else {
              this.qrScannerComponent.chooseCamera.next(videoDevices[0]);
          }
      }
  });

  this.qrScannerComponent.capturedQr.subscribe(result => {
      this.scanned = true;
      this.onCodeResult(result)
  });







  }


  onCodeResult(result: string) {

    this.qrResult = result

    // Si el usuario no hizo checkin, hace checkin. Va a location/detail/resultQR
    if (this.has_to_checkin){
      this.checkService.checkin(Number(this.qrResult))
      .subscribe( 
        (response) => {
          this.message = response["message"];
          if (response["success"]){
            setTimeout( () => this.router.navigate(['/location/detail', Number(result)]), 5000);
          }
          else{
            setTimeout( () => this.router.navigate(['/user']), 5000);
          }
        }
    )
    }
    // Si el usuario ya hizo checkin, hace checkout. Vuelve a user
    else{
      this.checkService.checkout(Number(this.qrResult))
      .subscribe( 
        (response) => {
          this.message = response["message"];
          setTimeout(() => this.router.navigate(['/user']), 5000);
        }
      )
    }
  }

  // Ver si lo puedo quitar
  toggleTryHarder(): void {
    this.tryHarder = !this.tryHarder;
  }

}
