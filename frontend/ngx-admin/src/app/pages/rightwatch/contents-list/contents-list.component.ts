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
      website: {
        title: 'website',
        type: 'number',
      },
/*      cat1_code: {
        title: 'cat1_code',
        type: 'string',
      },
      cat2_code: {
        title: 'cat2_code',
        type: 'string',
      },
      */
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
      payment: {
        title: 'payment',
        type: 'string',
      },
      seller: {
        title: 'seller',
        type: 'string',
      },
      partnership: {
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

  source1: LocalDataSource = new LocalDataSource();
  source: ServerDataSource;

/*  constructor(private service: SmartTableData) {
    const data = this.service.getData();
    this.source.load(data);
  }
  */
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
    endPoint: "http://127.0.0.1:5555/api/v1/post?limit=",
    sortFieldKey: "cat1_code",
    sortDirKey: "order",
    pagerPageKey: "offset",
    pagerLimitKey: "limit",
    totalKey: "total",
    dataKey: "data",
  }

  constructor(http: HttpClient) {
//    this.source = new ServerDataSource(http, { endPoint: 'https://jsonplaceholder.typicode.com/photos' });
    this.source = new ServerDataSource(http, this.conf)
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }
}