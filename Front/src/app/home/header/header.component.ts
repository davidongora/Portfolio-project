import { Component, inject, TemplateRef } from '@angular/core';
import { NgForm } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar'; // Import MatSnackBar
import { ApiService } from '../../api.service';
import { first, catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
  ],
})
export class HeaderComponent {
  isLoading = false;

  // Inject services using Angular's inject method for standalone components
  private apiService = inject(ApiService);
  private dialog = inject(MatDialog);
  private snackBar = inject(MatSnackBar); // Inject MatSnackBar

  // Method to open the dialog using the click event to get the position
  openDialog(event: MouseEvent, templateRef: TemplateRef<any>): void {
    const dialogPosition = {
      top: `${event.clientY}px`,
      left: `${event.clientX}px`
    };

    this.dialog.open(templateRef, {
      // width: '300px', // Customize modal width
      // position: dialogPosition, // Set position next to where it was clicked
    });
  }

  // Method to close the dialog from within the modal
  closeDialog(dialogRef: MatDialogRef<any>): void {
    dialogRef.close();
  }

  // Show toast messages
  private showToast(message: string, action: string = 'Close') {
    this.snackBar.open(message, action, {
      duration: 3000, // Duration in milliseconds
      horizontalPosition: 'right', // Toast position
      verticalPosition: 'top', // Toast position
    });
  }

  // Register method handler
  onRegister(signupForm: NgForm, dialogRef: MatDialogRef<any>) {
    if (!signupForm.valid) {
      return;
    }

    const { first_name, last_name, email, password, number } = signupForm.value;
    this.isLoading = true;

    this.apiService.register(first_name, last_name, email, password, number)
      .pipe(
        first(),
        catchError((error: HttpErrorResponse) => {
          this.isLoading = false;
          console.error('Registration failed', error);
          this.showToast('Failed to register user. Please try again.');
          return throwError(() => new Error('Failed to register user'));
        })
      )
      .subscribe({
        next: (response: any) => {
          console.log('Registration successful', response);
          this.isLoading = false;
          this.showToast('Registration successful!');
          this.closeDialog(dialogRef);
        },
        error: (err) => {
          console.error('Registration error:', err);
          this.isLoading = false;
          this.showToast('Registration error. Please try again.');
        }
      });
  }

  // Login method handler
  onLogin(loginForm: NgForm, dialogRef: MatDialogRef<any>) {
    if (!loginForm.valid) {
      return;
    }

    const { email, password } = loginForm.value;
    this.isLoading = true;

    this.apiService.login(email, password)
      .pipe(
        first(),
        catchError((error: HttpErrorResponse) => {
          this.isLoading = false;
          console.error('Login failed', error);
          this.showToast('Failed to login. Please try again.');
          return throwError(() => new Error('Failed to login'));
        })
      )
      .subscribe({
        next: (response: any) => {
          console.log('Login successful', response);
          this.isLoading = false;
          this.showToast('Login successful!');
          this.closeDialog(dialogRef);
        },
        error: (err) => {
          console.error('Login error:', err);
          this.isLoading = false;
          this.showToast('Login error. Please try again.');
        }
      });
  }
}
