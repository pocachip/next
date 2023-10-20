import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { RightwatchComponent } from './rightwatch.component';
import { ContentsListComponent } from './contents-list/contents-list.component'
import { PostListComponent } from './post-list/post-list.component'
import { CheckListComponent } from './check-list/check-list.component'
import { CheckListDetailComponent } from './check-list-detail/check-list-detail.component';

const routes: Routes = [{
  path: '',
  component: RightwatchComponent,
  children: [
    {
      path: 'contents-list',
      component: ContentsListComponent,
    },
    {
      path: 'check-list',
      component: CheckListComponent,
    },
    {
      path: 'check-list-detail/:id',
      component: CheckListDetailComponent,
    },
    {
      path: 'post-list',
      component: PostListComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})

export class RightwatchRoutingModule { }

export const routedComponents = [
  RightwatchComponent, 
  ContentsListComponent,
  CheckListComponent,
  PostListComponent,
];