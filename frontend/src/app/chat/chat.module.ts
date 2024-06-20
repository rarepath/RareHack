import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatComponent } from './chat.component';
import { RouterModule } from '@angular/router';
import { AppModule } from '../app.module';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    ChatComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    AppModule,
    FormsModule
  ]
})
export class ChatModule { }
