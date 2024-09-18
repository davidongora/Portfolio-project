import { Component, TemplateRef } from '@angular/core';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { ButtonsComponent } from '../buttons/buttons.component';
import { FormGroup } from '@angular/forms';
// import { FormModule } from '@coreui/angular';
import {NgForm} from '@angular/forms';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatDialogModule, 
    MatButtonModule,
    ButtonsComponent,
    // FormModule
  ],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  constructor(public dialog: MatDialog) {}

  // Method to open the dialog using the click event to get the position
  openDialog(event: MouseEvent, templateRef: TemplateRef<any>): void {
    const dialogPosition = {
      top: `${event.clientY}px`,
      left: `${event.clientX}px`
    };

    this.dialog.open(templateRef, {
      width: '300px', // Customize modal width
      position: dialogPosition, // Set position next to where it was clicked
    });
  }

  // Method to close the dialog from within the modal
  closeDialog(dialogRef: any): void {
    dialogRef.close();
  }
}
