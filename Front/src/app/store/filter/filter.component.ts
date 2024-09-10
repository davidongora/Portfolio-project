import { NgFor } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-filter',
  standalone: true,
  imports: [NgFor, FormsModule ],
  templateUrl: './filter.component.html',
  styleUrl: './filter.component.css'
})
export class FilterComponent {


  public gender: any[] = ['Male', 'Female']
  public AgeGroup: any[] = ['Adult', 'Children']
  public price: number = 50; 
  public size: any[] = ['Small', 'Medium', 'Large']
}
