import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { RightwatchComponent } from './rightwatch.component';
import { ContentsListComponent } from './contents-list/contents-list.component'

const routes: Routes = [{
  path: '',
  component: RightwatchComponent,
  children: [
    {
      path: 'contents-list',
      component: ContentsListComponent,
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
];