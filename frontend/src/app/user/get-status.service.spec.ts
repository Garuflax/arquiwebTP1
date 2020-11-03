import { TestBed } from '@angular/core/testing';

import { GetStatusService } from './get-status.service';

describe('GetStatusService', () => {
  let service: GetStatusService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GetStatusService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
