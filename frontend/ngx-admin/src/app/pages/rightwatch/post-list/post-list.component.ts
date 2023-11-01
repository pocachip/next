import { Component } from '@angular/core';
import { ServerDataSource } from 'ng2-smart-table';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'ngx-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.scss']
})
export class PostListComponent {

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
      website: {
        title: 'website',
        type: 'number',
        withd: '2px',
      },
      cat1_code: {
        title: 'cat1_code',
        type: 'string',
      },
      cat2_code: {
        title: 'cat2_code',
        type: 'string',
      },
      cat1_title: {
        title: 'cat1_title',
        type: 'string',
      },
      cat2_title: {
        title: 'cat2_title',
        type: 'string',
      },
      idx: {
        title: 'idx',
        type: 'string',
      },
      txt: {
        title: 'txt',
        type: 'string',
      },
      lvl19: {
        title: 'lvl19',
        type: 'string',
      },
      price: {
        title: 'payment',
        type: 'string',
      },
      seller: {
        title: 'seller',
        type: 'string',
      },
      partner: {
        title: 'partnership',
        type: 'string',
      },
      attach_file_size: {
        title: 'attach_file_size',
        type: 'string',
      },
      item_url: {
        title: 'item_url',
        type: 'string',
      },
      last_update: {
        title: 'last_update',
        type: 'string',
      },
    },
  };

  source: ServerDataSource;

 conf ={ 
    endPoint: "http://127.0.0.1:5555/api/v1/post",
    pagerPageKey: "page",
    pagerLimitKey: "limit",
    totalKey: "total",
    dataKey: "data",
    /*
    sortFieldKey: "cat1_code",
    sortDirKey: "order",
    */
  }

  constructor(http: HttpClient) {
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
