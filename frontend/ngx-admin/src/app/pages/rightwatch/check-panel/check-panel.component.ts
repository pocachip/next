import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { takeWhile } from 'rxjs/operators';
import { ContentsListComponent } from '../contents-list/contents-list.component';
import {CheckListDetailComponent} from '../check-list-detail/check-list-detail.component'

@Directive({selector: '[ngxPanel]'})
export class PanelDirective {
  @Input() id!: string;
}

@Component({
  selector: 'ngx-check-panel',
  templateUrl: './check-panel.component.html',
  styleUrls: ['./check-panel.component.scss']
})

export class CheckPanelComponent implements OnDestroy {

  @ViewChild(ContentsListComponent) content_list: any; 
  @ViewChild(CheckListDetailComponent) check_list: any; 
  @ViewChild(PanelDirective)
  set pane(v: PanelDirective) {
    setTimeout(() => {
      this.selectedPane = v.id;
    }, 0);
  }

  private alive = true;
  contentid: string = '';

  selectedPane: string = '';
  shouldShow = true;
  toggle() {
    this.shouldShow = !this.shouldShow;
  }

  changeContent(c_id: string){
    console.log("Pannel receive from chile: changeContents!!")
    setTimeout(() => {
      this.contentid = c_id;
    }, 0);
  }


  constructor() { }

  ngOnDestroy() {
    this.alive = false;
  }

  ngAfterViewInit(){

  }
}
