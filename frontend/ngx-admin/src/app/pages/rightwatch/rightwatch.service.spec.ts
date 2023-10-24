import { TestBed } from '@angular/core/testing';

import { RightwatchService } from './rightwatch.service';

describe('RightwatchService', () => {
  let service: RightwatchService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RightwatchService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
