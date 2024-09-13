import { Component } from '@angular/core';

@Component({
  selector: 'app-survey',
  standalone: true,
  imports: [],
  templateUrl: './survey.component.html',
  styleUrl: './survey.component.css'
})
export class SurveyComponent {

  constructor() {}

  ngOnInit(): void {
    this.openSurvey();
  }

  openSurvey(): void {
    const surveyUrl = 'https://oregonstate.qualtrics.com/jfe/form/SV_eRScOV0i4dDfmE6'; // Replace with your survey URL
    window.open(surveyUrl, '_blank');
  }

}
