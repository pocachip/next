import { Component, OnDestroy, Directive, Input, ViewChild } from '@angular/core';
import { ServerDataSource} from 'ng2-smart-table';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'ngx-check-list',
  templateUrl: './check-list.component.html',
  styleUrls: ['./check-list.component.scss']
})
export class CheckListComponent {
  @Input()
    get contentID(): string { return this._contentID;}
    set contentID(c_id: string){
      this._contentID = c_id;
    }
  
  private _contentID  = '';

  settings = {
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      id: {
        title: 'ID',
        type: 'number',
      },
      content_id: {
        title: '콘텐츠ID',
        type: 'number',
      },
      post_id: {
        title: 'post_id',
        type: 'string',
      },
      post_idx: {
        title: 'post_idx',
        type: 'string',
      },
      post_txt: {
        title: 'idx',
        type: 'string',
      },
      status: {
        title: 'status',
        type: 'integer',
      },
      first_time: {
        title: 'first_time',
        type: 'date-time',
      },
      update_time: {
        title: 'update_time',
        type: 'date-time',
      },
    },
    pager: {
      display : true,
      perPage: 20,
    },
  };

  source: ServerDataSource;


  conf ={ 
    endPoint: "http://127.0.0.1:5555/api/v1/check-list",
    pagerPageKey: "page",
    pagerLimitKey: "limit",
    totalKey: "total",
    dataKey: "data",
    /*
    sortFieldKey: "id",
    sortDirKey: "order",
    */
  }

  constructor(http: HttpClient){
    this.source = new ServerDataSource(http, this.conf)
  }
  

  onSearch(query: string = '') {
    this.source.setFilter([
      // fields we want to include in the search
      {
        field: 'id',
        search: query
      },
      {
        field: 'title',
        search: query
      },
    ], false); 
  // second parameter specifying whether to perform 'AND' or 'OR' search 
  // (meaning all columns should contain search query or at least one)
  // 'AND' by default, so changing to 'OR' by setting false here
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }
}