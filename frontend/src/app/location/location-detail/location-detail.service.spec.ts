import { TestBed } from '@angular/core/testing';

import { LocationDetailService } from './location-detail.service';

describe('LocationDetailService', () => {
  let service: LocationDetailService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LocationDetailService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
