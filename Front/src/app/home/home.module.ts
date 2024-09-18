import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeRoutingModule } from './home-routing.module';
// import { HttpClientModule } from '@angular/common/http'; // <-- Import HttpClientModule


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    HomeRoutingModule,
    // HttpClientModule
  ]
})
export class HomeModule { }
