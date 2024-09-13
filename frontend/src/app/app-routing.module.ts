import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ChatComponent } from './chat/chat.component';
import { WhitepaperComponent } from './whitepaper/whitepaper.component';
import { SurveyComponent } from './survey/survey.component';


export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'chat', component: ChatComponent },
    // { path: 'about-us', component: AboutUsComponent},
    { path: 'whitepaper', component: WhitepaperComponent},
    { path: 'survey', component: SurveyComponent},
    {path: '**', redirectTo: '', pathMatch: 'full'}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
