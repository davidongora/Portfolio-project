import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EndpointsService {

  constructor() { }

  public static CART_MAIN_CONTEXT = 'cart/';
  public static ORDER_ITEMS_MAIN_CONTEXT = 'order-items/';
  public static ORDER_MAIN_CONTEXT = 'orders/';
  public static PRODUCT_FILTERS_MAIN_CONTEXT = 'product_filters/';
  public static PRODUCTS_MAIN_CONTEXT = 'products/';
  public static USER_MAIN_CONTEXT = 'users/';
  public static WISHLIST_MAIN_CONTEXT = 'wishlist/';


  

  public static endpoint = {
    

    // ORDER_ITEMS

    // ORDERS

    // PRODUCT_FILTERS


    // PRODUCTS

    // USER
    LOGIN_USER: `${EndpointsService.CART_MAIN_CONTEXT}/cart/add/`, 
    REGISTER_USER: `${EndpointsService.CART_MAIN_CONTEXT}/cart/add/`, 

    //WISHLIST 
    // LOGIN_USER: `${EndpointsService.CART_MAIN_CONTEXT}/cart/add/`, 
    


  }
  
}
