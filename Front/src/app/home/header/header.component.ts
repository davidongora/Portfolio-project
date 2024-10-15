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
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const driverObj = driver({
  showProgress: true,
  animate: true,  
  doneBtnText: 'Finish', 
  nextBtnText: 'Next',  
  prevBtnText: 'Previous',  

  steps: [
    // { element: '#title', popover: { title: 'FashionForAll', description: 'Description' } },
    { element: '#orders', popover: { title: 'orders', description: 'Description' } },
    { element: '#contact', popover: { title: 'contact', description: 'Description' } },
    { element: '#title', popover: { title: 'FashionForAll', description: 'Description' } },
  ]
});

driverObj.drive();
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

  // Register service worker and request permission for push notifications
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    navigator.serviceWorker.register('/service-worker.js').then(registration => {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: this.urlBase64ToUint8Array('BKL0DcVViUJXNlPcmloYUzrvdrqm9cf7XzPrnED3c2oz_GRk3Zgn3u6MNwwRJVL4-P7-xe4UglvAnfE6wK8JGQM') // Replace with your VAPID public key
          }).then(subscription => {
            const pushSubscription = JSON.stringify(subscription);

            // Proceed with user registration along with the subscription data
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
          }).catch(error => {
            console.error('Push subscription failed:', error);
            this.isLoading = false;
            this.showToast('Push subscription failed. Please try again.');
          });
        } else {
          this.isLoading = false;
          this.showToast('Push notifications permission denied.');
        }
      });
    }).catch(error => {
      console.error('Service worker registration failed:', error);
      this.isLoading = false;
      this.showToast('Service worker registration failed. Please try again.');
    });
  } else {
    this.isLoading = false;
    this.showToast('Push notifications are not supported in your browser.');
  }
}

// Helper function to convert the VAPID public key to Uint8Array
private urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
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
