import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { takeWhile } from 'rxjs/operators';
import { ContentsListComponent } from '../content-panel/contents-list/contents-list.component';
import {CheckListDetailComponent} from './check-list-detail/check-list-detail.component'

interface con_interface {
  id: string;
  title: string;
}

@Component({
  selector: 'ngx-check-panel',
  templateUrl: './check-panel.component.html',
  styleUrls: ['./check-panel.component.scss']
})

export class CheckPanelComponent implements OnDestroy {

  @ViewChild(ContentsListComponent) content_list: any; 
  @ViewChild(CheckListDetailComponent) check_list: any; 

  private alive = true;
  content: con_interface ={id:'1', title:''};

  changeContent(c_in: con_interface){
    console.log("Parent changeContent");
    this.content = c_in;
  }

  constructor() { }

  ngOnDestroy() {
    this.alive = false;
  }

  ngAfterViewInit(){
  }
}
