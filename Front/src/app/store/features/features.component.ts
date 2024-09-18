import { Component, OnInit, TemplateRef } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ApiService } from '../../api.service'; // Ensure the path is correct
import { first, Subscription } from 'rxjs';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { NgFor, NgIf } from '@angular/common';
import { FilterComponent } from '../filter/filter.component';

@Component({
  selector: 'app-features',
  standalone: true,
  imports: [FilterComponent, NgFor, NgIf, MatDialogModule, MatButtonModule],
  templateUrl: './features.component.html',
  styleUrls: ['./features.component.css'] // Ensure the styleUrl is correct
})
export class FeaturesComponent implements OnInit {
  products: any[] = []; 
  isLoading: boolean = true;

  private unsubscribe: Subscription[] = [];
  pageSize = 6; 
  currentPage = 1;
  pagedProducts: any[] = [];

  constructor(private apiService: ApiService, public dialog: MatDialog) {}

  ngOnInit(): void {
    this.productslist(); 
  }

  productslist = () => {
    this.isLoading = true;
    console.log("Fetching products...");

    const handoversub = this.apiService.getProducts()
      .pipe(first())
      .subscribe({
        next: (response: any) => {
          this.products = response;
          this.updatePagedProducts();
          this.isLoading = false;
        },
        error: (err) => {
          this.isLoading = false;
          console.error(err);
        }
      });

    this.unsubscribe.push(handoversub);
  }

  updatePagedProducts() {
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    this.pagedProducts = this.products.slice(startIndex, endIndex);
  }

  changePage(page: number) {
    this.currentPage = page;
    this.updatePagedProducts();
  }

  get totalPages() {
    return Math.ceil(this.products.length / this.pageSize);
  }

  openDialog(templateRef: TemplateRef<any>, item: any): void {
    this.dialog.open(templateRef, {
      // data: item, // Passing selected product data to the modal
      // width: '600px',
      // height: '500px',
      // panelClass: 'custom-dialog-container'
    });
  }
  

  closeDialog(): void {
    this.dialog.closeAll(); // Close all dialogs
  }
}
