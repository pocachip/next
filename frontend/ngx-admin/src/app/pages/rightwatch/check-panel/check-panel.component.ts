import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { takeWhile } from 'rxjs/operators';

@Directive({selector: 'pane'})
export class Pane {
  @Input() id!: string;
}

@Component({
  selector: 'ngx-check-panel',
  templateUrl: './check-panel.component.html',
  styleUrls: ['./check-panel.component.scss']
})

export class CheckPanelComponent implements OnDestroy {
  @ViewChild(Pane)
    set pane(v: Pane) {
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
