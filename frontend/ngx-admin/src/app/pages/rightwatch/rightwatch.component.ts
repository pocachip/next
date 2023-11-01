import { Component } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

@Component({
  selector: 'ngx-rightwatch',
  template: `<router-outlet></router-outlet>`,
})
export class RightwatchComponent {
  constructor(private themeService: NbThemeService) {
    this.themeService.changeTheme('cosmic');
  }
}
