import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-whitepaper',
  standalone: true,
  imports: [],
  templateUrl: './whitepaper.component.html',
  styleUrls: ['./whitepaper.component.css']
})
export class WhitepaperComponent {
  constructor(private router: Router) {}



  
  openPdf(): void {
    const pdfUrl = 'https://drive.google.com/file/d/16KfXBr_qv6kiVxxPIYuoLCeE0_kTUuaW/view?usp=sharing'; // Replace with your PDF URL
    window.open(pdfUrl, '_blank');
    this.router.navigate(['/']);  // Redirect back to home
  }
}
