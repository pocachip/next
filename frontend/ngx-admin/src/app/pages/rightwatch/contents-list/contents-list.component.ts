import { Component } from '@angular/core';
import { LocalDataSource, ServerDataSource} from 'ng2-smart-table';
//import { ServerSourceConf } from './server-source.conf';
import { HttpClient } from '@angular/common/http';

import { SmartTableData } from '../../../@core/data/smart-table';

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

 /*
 conf: ServerSourceConf;
    protected static readonly SORT_FIELD_KEY = "_sort";
    protected static readonly SORT_DIR_KEY = "_order";
    protected static readonly PAGER_PAGE_KEY = "_page";
    protected static readonly PAGER_LIMIT_KEY = "_limit";
    protected static readonly FILTER_FIELD_KEY = "#field#_like";
    protected static readonly TOTAL_KEY = "x-total-count";
    protected static readonly DATA_KEY = "";
*/
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

  constructor(http: HttpClient) {
   //  this.source = new ServerDataSource(http, { endPoint: 'http://127.0.0.1:5555/api/v1/contents-list' });
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