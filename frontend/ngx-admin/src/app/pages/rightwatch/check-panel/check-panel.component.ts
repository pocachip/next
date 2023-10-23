import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { takeWhile } from 'rxjs/operators';

@Directive({selector: '[ngxPanel]'})
export class Panel {
  @Input() id!: string;
}

@Component({
  selector: 'ngx-check-panel',
  templateUrl: './check-panel.component.html',
  styleUrls: ['./check-panel.component.scss']
})

export class CheckPanelComponent implements OnDestroy {
  @ViewChild(Panel)
    set pane(v: Panel) {
    setTimeout(() => {
      this.selectedPane = v.id;
    }, 0);
  }
  selectedPane: string = '';
  shouldShow = true;
  toggle() {
    this.shouldShow = !this.shouldShow;
  }

  private alive = true;

  constructor() { }

  ngOnDestroy() {
    this.alive = false;
  }
}
