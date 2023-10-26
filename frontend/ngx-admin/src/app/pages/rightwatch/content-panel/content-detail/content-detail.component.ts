import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { RightwatchService } from '../../rightwatch.service';
import { LocalDataSource } from 'ng2-smart-table';
 
export interface IDataApi {
  code : number;
  data : any;
  limit : number;
  offset: number;
  total: number;
}

export interface IContentDetail {
  id : number;
  title : string;
  actors : string;
  director: string;
  genre: string;
  price : string;
  synop : string;
  enddate : string;
  p_url : string;
}

@Component({
  selector: 'ngx-content-detail',
  templateUrl: './content-detail.component.html',
  styleUrls: ['./content-detail.component.scss']
})
export class ContentDetailComponent implements OnInit {
  @Input()
    get ID(): string { return this._id;}
    set ID(instr: string){
      if(instr){
        this._id = instr;
        this.getData();
      }
    }

  _id:string='';
  _data: IContentDetail;

  constructor(private http: HttpClient, private apiService: RightwatchService) {
    console.log('content detail comp constructor')
  }

  getData(){
      if(this._id){ 
        let urlin = `http://127.0.0.1:5555/api/v1/kta-content/${this._id}`;
        this.apiService.getData(urlin).subscribe((data) =>{
          this._data = data.data;
        });
      }
  }

  ngOnInit(): void {
    console.log("ngOnInit");
    console.log(this);
    this.getData();
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }
  
}

/*

  settings = {
    editable: false,
    noDataMessage: 'No data could be found here.',
    actions: {
        delete: false,
        add: false,
        edit: false,
        position: 'right'
    },
    columns: {
      id: {
        title: 'ID',
        type: 'number',
      },
      genre: {
        title: '장르',
        type: 'string',
      },
      title: {
        title: '제목',
        type: 'string',
      },
      actors: {
        title: '출연진',
        type: 'string',
      },
      director: {
        title: '감독',
        type: 'string',
      },
      price: {
        title: '가격',
        type: 'integer',
      },
      enddate: {
        title: '판권기간',
        type: 'date-time',
      },
      synop: {
        title: '줄거리',
        type: 'string',
      },
      p_url: {
        title: '이미지URL',
        type: 'string',
      },
    },
    pager: {
      display : true,
      perPage: 20,
    },
  };

  conf ={ 
//    endPoint: "http://127.0.0.1:5555/api/v1/check-list?where1=content_id%3A1",
  }

*/