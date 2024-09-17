import { FilterComponent } from '../filter/filter.component';
import { Component, OnInit, NgModule } from '@angular/core';
import { NgFor } from '@angular/common';
import { ApiService } from '../../api.service'; // Make sure the path is correct
import { first, Subscription } from 'rxjs';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule

@Component({
  selector: 'app-features',
  standalone: true,
  imports: [FilterComponent, NgFor],
  templateUrl: './features.component.html',
  styleUrl: './features.component.css'
})
export class FeaturesComponent {
  products: any[] = []; 
  isLoading: boolean = false;

  private unsubscribe: Subscription[] = [];
  pageSize = 6; 
  currentPage = 1;
  pagedProducts: any[] = [];
  constructor(private apiService: ApiService, ) {
    this.updatePagedProducts();
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

  ngOnInit(): void {
    this.productslist(); 
  }

  productslist = () =>{
    this.isLoading = true;
    console.log("function initiated");

    const handoversub = this.apiService.getProducts()
      .pipe(first())
      .subscribe({
        next: (response: any) => {
          this.products = response;
          this.updatePagedProducts(); 
          // console.log(response);
        },
        error:(err) => {
          this.isLoading = false;
          console.log(err);
        }
      });
    this.unsubscribe.push(handoversub);
  }
}
