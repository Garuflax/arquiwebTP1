import { TestBed } from '@angular/core/testing';

import { AddLocationService } from './add-location.service';

describe('AddLocationService', () => {
  let service: AddLocationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AddLocationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
