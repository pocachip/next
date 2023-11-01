import { Component, Input, OnInit, ViewChild, Directive, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { ServerDataSource } from 'ng2-smart-table';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';

interface con_interface {
  id: string;
  title: string;
}

@Component({
  selector: 'ngx-check-list-detail',
  templateUrl: './check-list-detail.component.html',
  styleUrls: ['./check-list-detail.component.scss']
})
export class CheckListDetailComponent implements OnInit {
  @ViewChild('mass_timings') mass_timings: ElementRef<InnerHTML>;
  @Input()
    get content(): con_interface { return this._content;}
    set content(in_content: con_interface){
      if(in_content){
        this._content = in_content;
        this.setEndPoint(this._content.id);
      }
    }

  _content:con_interface={id:'1',title:''};
  settings = {
    editable: false,
    noDataMessage: 'No data could be found here.',
    actions: {
        delete: false,
        add: false,
        edit: false,
        position: 'right'
    },
    /*
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
    */
    columns: {
      id: {
        title: 'ID',
        type: 'number',
        filter: false,
      },
      content_id: {
        title: '콘텐츠ID',
        type: 'number',
        filter: false,
      },
      post_id: {
        title: 'post_id',
        type: 'string',
        width: '5px',
        filter: false,
      },
      post_idx: {
        title: 'post_idx',
        type: 'string',
        filter: false,
      },
      post_txt: {
        title: '게시글제목',
        type: 'html',
        valuePrepareFunction: (title, row) => {
            return this.sanitizer.bypassSecurityTrustHtml(this.changeRed(title));
        },
        filter: false,
      },
      status: {
        title: 'status',
        type: 'integer',
        filter: false,
      },
      first_time: {
        title: 'first_time',
        type: 'date-time',
        filter: false,
      },
      update_time: {
        title: 'update_time',
        type: 'date-time',
        filter: false,
      },
    },
    pager: {
      display : true,
      perPage: 20,
    },
  };

  conf ={ 
//    endPoint: "http://127.0.0.1:5555/api/v1/check-list?where1=content_id%3A1",
    endPoint: "http://127.0.0.1:5555/api/v1/check-list",
    pagerPageKey: "page",
    pagerLimitKey: "limit",
    totalKey: "total",
    dataKey: "data",
  }
  source: ServerDataSource;
  isAdmin: boolean = false;

  constructor(private sanitizer: DomSanitizer, private http: HttpClient) { 
  }

  private changeRed(instr: string): string {
    let repl_word = '<font color="red">'+this._content.title+"</font>";
    return instr.replace(this.content.title, repl_word) 
  }
  ngOnInit(): void {
    this.getData();
    this.hideColumnForUser();
  }

  hideColumnForUser(){
    if(!this.isAdmin){
        delete this.settings.columns.id;
        delete this.settings.columns.content_id;
        //delete this.settings.columns.post_id;
        delete this.settings.columns.post_idx;
        delete this.settings.columns.status;
        delete this.settings.columns.first_time;
        delete this.settings.columns.update_time;
    }
  }
  getData(): void {
    this.source = new ServerDataSource(this.http, this.conf)
  }

  reload(){
    this.getData();
  }

  setEndPoint(contentid: string){
    this.conf.endPoint = "http://127.0.0.1:5555/api/v1/check-list?where1=content_id%3A"+this._content.id;
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
