import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { RightwatchComponent } from './rightwatch.component';
import { ContentsListComponent } from './content-panel/contents-list/contents-list.component'
import { ContentDetailComponent } from './content-panel/content-detail/content-detail.component';
import { PostListComponent } from './post-list/post-list.component'
import { CheckListComponent } from './check-panel/check-list/check-list.component'
import { CheckListDetailComponent } from './check-panel/check-list-detail/check-list-detail.component';
import { CheckPanelComponent } from './check-panel/check-panel.component'
import { ContentPanelComponent } from './content-panel/content-panel.component';

const routes: Routes = [{
  path: '',
  component: RightwatchComponent,
  children: [
    {
      path: 'content-panel',
      component: ContentPanelComponent,
    },
    {
      path: 'contents-list',
      component: ContentsListComponent,
    },
    {
      path: 'content-detail',
      component: ContentDetailComponent,
    },
    {
      path: 'check-list',
      component: CheckListComponent,
    },
    {
      path: 'check-list-detail',
      component: CheckListDetailComponent,
    },
    {
      path: 'post-list',
      component: PostListComponent,
    },
    {
      path: 'check-panel',
      component: CheckPanelComponent,
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