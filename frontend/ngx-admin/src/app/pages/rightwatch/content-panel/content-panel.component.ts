import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { ContentsListComponent } from './contents-list/contents-list.component';
import { ContentDetailComponent } from './content-detail/content-detail.component';

@Component({
  selector: 'ngx-content-panel',
  templateUrl: './content-panel.component.html',
  styleUrls: ['./content-panel.component.scss']
})
export class ContentPanelComponent implements OnDestroy {

  @ViewChild(ContentsListComponent) contents_list: any; 
  @ViewChild(ContentDetailComponent) content_detail: any; 

  private alive = true;
  ID :string = '';

  constructor() {
   }

  changeContent(event: any){
    this.ID = event.id;
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
