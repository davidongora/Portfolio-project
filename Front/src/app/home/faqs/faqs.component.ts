import { Component } from '@angular/core';


@Component({
  selector: 'app-faqs',
  standalone: true,
  imports: [],
  templateUrl: './faqs.component.html',
  styleUrl: './faqs.component.css'
})
export class FaqsComponent {
  private expandedItemId: string | null = null;

  toggleCollapse(id: string): void {
    this.expandedItemId = this.expandedItemId === id ? null : id;
  }

  isExpanded(id: string): boolean {
    return this.expandedItemId === id;
  }
}
