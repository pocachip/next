import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ServerDataSource} from 'ng2-smart-table';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'ngx-contents-list',
  templateUrl: './contents-list.component.html',
  styleUrls: ['./contents-list.component.scss']
})

export class ContentsListComponent { 
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
        width: '5px',
      },
      title: {
        title: 'contents_name',
        type: 'string',
      },
    },
    pager: {
      display : true,
      perPage: 20,
    },
  };

  source: ServerDataSource;

  conf ={ 
    endPoint: "http://127.0.0.1:5555/api/v1/contents-list",
    totalKey: "total",
    dataKey: "data",
    pagerPageKey: "page",
    pagerLimitKey: "limit",
    /*
    sortFieldKey: "id",
    sortDirKey: "order",
    */
  }

  constructor(http: HttpClient){
    this.source = new ServerDataSource(http, this.conf);
  }

  onSearch(query: string = '') {
  this.source.setFilter([
    // fields we want to include in the search
    {
      field: 'title',
      search: query,
    },
  ], false); 
  // second parameter specifying whether to perform 'AND' or 'OR' search 
  // (meaning all columns should contain search query or at least one)
  // 'AND' by default, so changing to 'OR' by setting false here
  }

  onUserRowSelect(event): void {
    console.log(event.data.id);
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }
}