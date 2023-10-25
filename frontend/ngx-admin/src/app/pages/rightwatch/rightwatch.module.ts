import { NgModule } from '@angular/core';
import { NbCardModule, NbIconModule, NbInputModule, NbTreeGridModule } from '@nebular/theme';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import { ThemeModule } from '../../@theme/theme.module';
import { RightwatchRoutingModule, routedComponents } from './rightwatch-routing.module';
import { CheckListComponent } from './check-panel/check-list/check-list.component';
import { PostListComponent } from './post-list/post-list.component';
import { CheckListDetailComponent } from './check-panel/check-list-detail/check-list-detail.component';
import { CheckPanelComponent } from './check-panel/check-panel.component';
import { ContentDetailComponent } from './content-panel/content-detail/content-detail.component';
import { ContentPanelComponent } from './content-panel/content-panel.component';

@NgModule({
  imports: [
    NbCardModule,
    NbTreeGridModule,
    NbIconModule,
    NbInputModule,
    ThemeModule,
    RightwatchRoutingModule,
    Ng2SmartTableModule,
  ],
  declarations: [
    ...routedComponents,
    CheckListComponent,
    PostListComponent,
    CheckListDetailComponent,
    CheckPanelComponent,
    ContentDetailComponent,
    ContentPanelComponent,
  ],
})
export class RightwatchModule { }
