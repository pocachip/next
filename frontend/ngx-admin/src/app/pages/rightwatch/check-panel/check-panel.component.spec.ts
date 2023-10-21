import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckPanelComponent } from './check-panel.component';

describe('CheckPanelComponent', () => {
  let component: CheckPanelComponent;
  let fixture: ComponentFixture<CheckPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CheckPanelComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CheckPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
