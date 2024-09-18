import { EndpointsService } from './endpoints.service';
import { HttpParams, HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private isLoadingSubject = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient, private endpointsService: EndpointsService) { }

  // Example: Fetch MyClaimsSummary
  public MyClaimsSummary(company_id: string): Observable<any> {
    this.isLoadingSubject.next(true);
    
    // Constructing URL using the EndpointsService
    const url = this.endpointsService.endpoint.GET_PRODUCTS;  // Example: Change this to the correct endpoint
    
    // Adding query params like `company_id`
    return this.http.get(`${url}?company_id=${company_id}`, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.isLoadingSubject.next(false);  // Set loading to false on success
        return response;
      }),
      catchError((fault: HttpErrorResponse) => {
        this.isLoadingSubject.next(false);  // Set loading to false on error
        return throwError(() => fault);
      })
    );
  }

  // Example: Fetch products with optional filters
  public getProducts(filters?: any): Observable<any> {
    this.isLoadingSubject.next(true);

    // Constructing URL for products
    const url = this.endpointsService.endpoint.GET_PRODUCTS;

    // If filters are passed, use them to create query params
    let params = new HttpParams();
    if (filters) {
      Object.keys(filters).forEach(key => {
        params = params.append(key, filters[key]);
      });
    }

    return this.http.get(url, { params }).pipe(
      map((response: any) => {
        this.isLoadingSubject.next(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.isLoadingSubject.next(false);
        return throwError(() => error);
      })
    );
  }
}
