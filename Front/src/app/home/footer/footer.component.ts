import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {

  public items = ['explore', 'Product', 'sell your producerNotifyConsumers', 'Pricing', 'Reviews']
  public footer_items = ['Privacy policy', 'Legal', 'Terms of service', 'Help center']

}
