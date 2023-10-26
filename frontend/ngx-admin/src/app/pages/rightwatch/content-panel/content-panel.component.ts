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
    console.log("constructor")
    console.log(this);
   }

  changeContent(event: any){
    console.log("Parent changeContent");
    this.ID = event.id;
    console.log(this);
  }

  ngOnDestroy() {
    this.alive = false;
  }


}
