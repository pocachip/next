import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckListDetailComponent } from './check-list-detail.component';

describe('CheckListDetailComponent', () => {
  let component: CheckListDetailComponent;
  let fixture: ComponentFixture<CheckListDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CheckListDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CheckListDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
