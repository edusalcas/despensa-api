import { TestBed } from '@angular/core/testing';

import { AlimentsService } from './aliments.service';

describe('AlimentsService', () => {
  let service: AlimentsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AlimentsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
