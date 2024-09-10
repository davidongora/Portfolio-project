import { Component } from '@angular/core';
import { ButtonsComponent } from '../buttons/buttons.component';
import { FormsModule } from '@angular/forms';
import { CommonModule, NgFor } from '@angular/common';

@Component({
  selector: 'app-reviews',
  standalone: true,
  imports: [ButtonsComponent, FormsModule, NgFor, CommonModule],
  templateUrl: './reviews.component.html',
  styleUrl: './reviews.component.css'
})
export class ReviewsComponent {
  slides = [0, 1, 2]; // Placeholder for slide data
  currentIndex = 0;
  translateX = '0%';
  dots = [0, 1, 2]; // Number of dots based on slides
  intervalId: any;

  ngOnInit(): void {
    this.startAutoSlide();
  }

  ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  startAutoSlide() {
    this.intervalId = setInterval(() => {
      this.nextSlide();
    }, 15000); // 15 seconds
  }

  goToSlide(index: number) {
    this.currentIndex = index;
    this.translateX = `-${index * 100}%`;
    this.resetInterval();
  }

  nextSlide() {
    this.currentIndex = (this.currentIndex + 1) % this.slides.length;
    this.translateX = `-${this.currentIndex * 100}%`;
  }

  resetInterval() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    this.startAutoSlide();
  }
}
