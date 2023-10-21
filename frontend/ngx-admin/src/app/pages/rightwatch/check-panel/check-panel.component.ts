import { Component, OnDestroy, ViewChild} from '@angular/core';
import { takeWhile } from 'rxjs/operators';

@Component({
  selector: 'ngx-check-panel',
  templateUrl: './check-panel.component.html',
  styleUrls: ['./check-panel.component.scss']
})
export class CheckPanelComponent implements OnDestroy {

  private alive = true;

  constructor() { }

  ngOnDestroy() {
    this.alive = false;
  }
}
