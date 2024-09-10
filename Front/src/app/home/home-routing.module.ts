import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { InfoComponent } from './info/info.component';
import { ButtonsComponent } from './buttons/buttons.component';
import { CustomersComponent } from './customers/customers.component';
import { WhatWeDoComponent } from './what-we-do/what-we-do.component';
import { ReviewsComponent } from './reviews/reviews.component';
import { FooterComponent } from './footer/footer.component';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { FaqsComponent } from './faqs/faqs.component';

const routes: Routes = [
  {
    path: 'home',
    component: HeaderComponent
  },
  {
    path: 'info',
    component: InfoComponent
  },
  {
    path: 'header',
    component: HeaderComponent
  },
  {
    path: 'button',
    component: ButtonsComponent
  },
  {
    path: 'customers',
    component: CustomersComponent
  },
  {
    path: 'what-we-do',
    component: WhatWeDoComponent
  },
  {
    path: 'reviews',
    component: ReviewsComponent
  },
  {
    path: 'footer',
    component: FooterComponent
  },
  {
    path: 'signup',
    component: SignupComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'faqs',
    component: FaqsComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule { }
