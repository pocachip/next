import { Component, Input, OnInit } from '@angular/core';

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
      }
    }

  _id:string='';

  constructor() { }

  ngOnInit(): void {
  }

}
