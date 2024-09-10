import { Component } from '@angular/core';
import {HeaderComponent} from '../header/header.component'
import { ButtonsComponent } from "../buttons/buttons.component";
@Component({
  selector: 'app-info',
  standalone: true,
  imports: [HeaderComponent, ButtonsComponent],
  templateUrl: './info.component.html',
  styleUrl: './info.component.css'
})
export class InfoComponent {

}
