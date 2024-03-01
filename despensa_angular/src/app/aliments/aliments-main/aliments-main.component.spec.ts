import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlimentsMainComponent } from './aliments-main.component';

describe('AlimentsMainComponent', () => {
  let component: AlimentsMainComponent;
  let fixture: ComponentFixture<AlimentsMainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AlimentsMainComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AlimentsMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
