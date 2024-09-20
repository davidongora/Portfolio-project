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

  private setLoading(loading: boolean): void {
    this.isLoadingSubject.next(loading);
  }

  public getProducts(): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.GET_PRODUCTS;
    return this.http.get(`${url}`, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to fetch products'));
      })
    );
  }

  public getProductsFilters(): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.GET_PRODUCT_FILTERS;
    return this.http.get(`${url}`, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to fetch product filters'));
      })
    );
  }

  public login(username: string, password: string): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.LOGIN_USER;
    return this.http.get(`${url}`, {
      params: { username, password },
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to login'));
      })
    );
  }

  public register(first_name: string, last_name: string, email: string, password: string, phone_number: string): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.REGISTER_USER;
    return this.http.post(`${url}`, {
      first_name, last_name, email, password, phone_number
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to register user'));
      })
    );
  }

  public addToCart(user_id: string, product_id: string, quantity: number): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.ADD_TO_CART;
    return this.http.post(`${url}`, {
      user_id, product_id, quantity
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to add item to cart'));
      })
    );
  }

  public createOrder(user_id: string, shipping_address: string, payment_method: string, cart_items: any[]): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.CREATE_ORDER;
    return this.http.post(`${url}`, {
      user_id, shipping_address, payment_method, cart_items
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to create order'));
      })
    );
  }

  public updateCart(cart_id: string, quantity: number): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.UPDATE_CART_ITEMS;
    return this.http.post(`${url}`, {
      cart_id, quantity
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to update cart'));
      })
    );
  }

  public removeFromCart(cart_id: string): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.REMOVE_FROM_CART;
    return this.http.post(`${url}`, {
      cart_id
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to remove item from cart'));
      })
    );
  }

  public viewCart(user_id: string): Observable<any> {
    this.setLoading(true);
    const url = this.endpointsService.endpoint.GET_CART_ITEMS;
    return this.http.get(`${url}`, {
      params: { user_id },
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    }).pipe(
      map((response: any) => {
        this.setLoading(false);
        return response;
      }),
      catchError((error: HttpErrorResponse) => {
        this.setLoading(false);
        return throwError(() => new Error('Failed to fetch cart items'));
      })
    );
  }
}
