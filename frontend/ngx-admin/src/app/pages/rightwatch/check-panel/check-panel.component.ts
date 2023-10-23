import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { takeWhile } from 'rxjs/operators';
import { ContentsListComponent } from '../contents-list/contents-list.component';
import {CheckListDetailComponent} from '../check-list-detail/check-list-detail.component'

@Component({
  selector: 'ngx-check-panel',
  templateUrl: './check-panel.component.html',
  styleUrls: ['./check-panel.component.scss']
})

export class CheckPanelComponent implements OnDestroy {

  @ViewChild(ContentsListComponent) content_list: any; 
  @ViewChild(CheckListDetailComponent) check_list: any; 

  private alive = true;
  contentid: string = '1';

  changeContent(c_id: string){
      this.contentid = c_id;
  }

  constructor() { }

  ngOnDestroy() {
    this.alive = false;
  }

  ngAfterViewInit(){

  }
}
