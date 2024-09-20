import { Injectable, OnDestroy } from '@angular/core';
import { HttpParams, HttpClient, HttpErrorResponse } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class EndpointsService   {


  constructor(public http: HttpClient ) {  }

  
  private apiUrl = 'http://127.0.0.1:8000/api/';  

  public static CART_MAIN_CONTEXT = 'cart';
  public static ORDER_ITEMS_MAIN_CONTEXT = 'order-items';
  public static ORDER_MAIN_CONTEXT = 'orders';
  public static PRODUCT_FILTERS_MAIN_CONTEXT = 'product_filters';
  public static PRODUCTS_MAIN_CONTEXT = 'products';
  public static USER_MAIN_CONTEXT = 'users';
  public static WISHLIST_MAIN_CONTEXT = 'wishlist';

  public endpoint = {
    // CART
    ADD_TO_CART: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/add`,
    REMOVE_FROM_CART: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/remove`,
    GET_CART_ITEMS: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/view`,
    UPDATE_CART_ITEMS: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/update`,

    // ORDER ITEMS
    ADD_ORDER_ITEM: `${this.apiUrl}${EndpointsService.ORDER_ITEMS_MAIN_CONTEXT}/add`,
    REMOVE_ORDER_ITEM: `${this.apiUrl}${EndpointsService.ORDER_ITEMS_MAIN_CONTEXT}/remove`,

    // ORDERS
    CREATE_ORDER: `${this.apiUrl}${EndpointsService.ORDER_MAIN_CONTEXT}/create`,
    GET_ORDERS: `${this.apiUrl}${EndpointsService.ORDER_MAIN_CONTEXT}/list`,
    GET_ORDERS_DETAILS: `${this.apiUrl}${EndpointsService.ORDER_MAIN_CONTEXT}/details`,

    
    // PRODUCT FILTERS
    GET_PRODUCT_FILTERS: `${this.apiUrl}${EndpointsService.PRODUCT_FILTERS_MAIN_CONTEXT}`,

    // PRODUCTS
    GET_PRODUCTS: `${this.apiUrl}${EndpointsService.PRODUCTS_MAIN_CONTEXT}/products/`,
    GET_PRODUCT_DETAILS: `${this.apiUrl}${EndpointsService.PRODUCTS_MAIN_CONTEXT}/details`,

    // USER
    LOGIN_USER: `${this.apiUrl}${EndpointsService.USER_MAIN_CONTEXT}/login/`,
    REGISTER_USER: `${this.apiUrl}${EndpointsService.USER_MAIN_CONTEXT}/register/`,

    
  };
}
