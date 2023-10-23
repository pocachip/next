import { Component, Input, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { ServerDataSource } from 'ng2-smart-table';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'ngx-check-list-detail',
  templateUrl: './check-list-detail.component.html',
  styleUrls: ['./check-list-detail.component.scss']
})
export class CheckListDetailComponent implements OnInit {
  @Input()
    get contentid(): string { return this._contentid;}
    set contentid(c_id: string){
      console.log("checklistdetail set func");
      console.log(c_id);
      this._contentid = c_id;
      this.setEndPoint(this._contentid);
    }
  
  _contentid: string  = '';

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

  conf ={ 
    //endPoint: "http://127.0.0.1:5555/api/v1/check-list?where1=content_id%3A",
    endPoint: "http://127.0.0.1:5555/api/v1/check-list",
    pagerPageKey: "page",
    pagerLimitKey: "limit",
    totalKey: "total",
    dataKey: "data",
  }
  source: ServerDataSource;

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) { 
    console.log("constructure")
  }

  ngOnInit(): void {
    this.getData();
    console.log(this);
  }
  
  getData(): void {
    this.source = new ServerDataSource(this.http, this.conf)
  }

  reload(){
    this.source.refresh();
  }

  setEndPoint(contentid: string){
    this.conf.endPoint = "http://127.0.0.1:5555/api/v1/check-list?where1=content_id%3A"+this._contentid;
    console.log("setEndPoint");
    console.log(this.conf.endPoint)
    this.reload();
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
