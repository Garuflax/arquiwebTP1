import { TestBed } from '@angular/core/testing';

import { InformService } from './inform.service';

describe('InformService', () => {
  let service: InformService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InformService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
