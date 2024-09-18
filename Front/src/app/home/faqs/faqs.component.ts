import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';


@Component({
  selector: 'app-faqs',
  standalone: true,
  imports: [NgFor, NgIf],
  templateUrl: './faqs.component.html',
  styleUrl: './faqs.component.css'
})
export class FaqsComponent {
  
  faqs = [
    { question: "What is Angular?", answer: "Angular is a platform and framework for building single-page client applications using HTML and TypeScript.", show: false },
    { question: "How do I install Angular?", answer: "You can install Angular using the Angular CLI by running `npm install -g @angular/cli` in your terminal.", show: false },
    { question: "What is a component in Angular?", answer: "A component controls a patch of the screen called a view and consists of HTML, CSS, and TypeScript files.", show: false },
  ];

  toggleFAQ(index: number): void {
    this.faqs[index].show = !this.faqs[index].show;
  }

}
