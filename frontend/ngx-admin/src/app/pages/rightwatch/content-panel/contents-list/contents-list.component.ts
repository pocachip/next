import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ServerDataSource, LocalDataSource} from 'ng2-smart-table';
import { HttpClient } from '@angular/common/http';
import { RightwatchService } from '../../rightwatch.service';

@Component({
  selector: 'ngx-contents-list',
  templateUrl: './contents-list.component.html',
  styleUrls: ['./contents-list.component.scss']
})

export class ContentsListComponent { 
  @Input()
    get selectedID(): string { return this._selectedID}
    set selectedID(selected: string){
      this._selectedID = selected;
    }
   
  @Output() selectedEvent = new EventEmitter<string>();

  private _selectedID  = '';

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
        width: '5px',
        filter: false,
      },
      title: {
        title: '콘텐츠명',
        type: 'string',
        filter: false,
      },
    },
    pager: {
      display : true,
      perPage: 20,
    },
  };

  source: ServerDataSource;
  source_local: LocalDataSource;

  conf ={ 
    endPoint: "http://127.0.0.1:5555/api/v1/kta-content",
    totalKey: "total",
    dataKey: "data",
    pagerPageKey: "page",
    pagerLimitKey: "limit",
    filterFieldKey: 'title' 
    /*
    filterFieldKey
    sortFieldKey: "id",
    sortDirKey: "order",
    */
  }

  constructor(private http: HttpClient, private apiService: RightwatchService){
    this.source = new ServerDataSource(http, this.conf);
  }

  getData(query:string): void {
    let urlin = '';
    if(1) {  //change later api
      if(query){
        urlin = "http://127.0.0.1:5555/api/v1/kta-content?where=title%3A"+query;
      } else {
        urlin = "http://127.0.0.1:5555/api/v1/kta-content";
      }
      this.conf.endPoint = urlin;
      this.source = new ServerDataSource(this.http, this.conf)
    } else {
      if(query){
        urlin = "http://127.0.0.1:5555/api/v1/kta-content?where=title%3A"+query;
      } else {
        urlin = "http://127.0.0.1:5555/api/v1/kta-content";
      }
      this.apiService.getData(urlin).subscribe((data) =>{
        this.source.load(data.data);
        this.source.refresh();
      });
    }
  }

  reload(query:string){
    this.getData(query);
  }

  setEndPoint(query: string){
    if(query){
      this.conf.endPoint = "http://127.0.0.1:5555/api/v1/kta-content?where=title%3A"+query;
    } else {
      this.conf.endPoint = "http://127.0.0.1:5555/api/v1/kta-content";
    }
    this.reload(query);
  }

  onSearch(query: string = '') {
//    this.setEndPoint(query);
    this.getData(query);

//    this.source.reset(true);  // reset your old filtered data 
//    this.source.setPage(1, false); // set page to 1 to start from beginning 
//    console.log(this);
//    this.source.setFilter([
//      // fields we want to include in the search
//      {
//        field: 'title',
//        search: query,
//      },
//    ], false); 
//    this.source.refresh();
//    
//    console.log(this);
//    console.log(query);
  // second parameter specifying whether to perform 'AND' or 'OR' search 
  // (meaning all columns should contain search query or at least one)
  // 'AND' by default, so changing to 'OR' by setting false here
  }

  onUserRowSelect(event): void {
    //console.log(event.data.id);
    //console.log("onUserRowSelect");
    //console.log(event);
    //this._selectedID= event.data.id;
    this._selectedID= event.data;
    this.selectedEvent.emit(this._selectedID)
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }
 
  FilterData():void {
    this.source.reset(true);  // reset your old filtered data 
    this.source.setPage(1, false); // set page to 1 to start from beginning 
/*
    let filterArr = this.getFilterArray(); // add a new filter data, but be careful to not sent any empty data, as it throws an exception 
    if (filterArr.length)
      this.source.setFilter(filterArr, false, false);
*/
    this.source.refresh(); // this will call the server with new filter and paginatio data
  }
/*
  getFilterArray() {  // setup new filter 
    let filterArray = [];
    if (this.filter.id)
      filterArray.push({ field: 'id', search: this.filter.id });
    if (this.filter.name)
      filterArray.push({ field: 'name', search: this.filter.name});

    return filterArray;  
  }
  */
  onCustomAction(event) {  // custom buttons code 
    switch (event.action) {
      case 'view-something':
      // put your code here 
      break;
      default:
      console.log('Not Implemented Action');
      break;
    }
  }
}