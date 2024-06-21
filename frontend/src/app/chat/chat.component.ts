import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ChatService } from './chat.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import TypeIt from 'typeit';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [RouterModule, FormsModule, CommonModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent {
    // user input, model selection, and current summary to send to api POST endpoint
    userInput: string = '';
    modelSelection: string = 'both';
    currentSummary: string = '';
    isThinking: boolean = false;

    // messages to be displayed
    messages: { sender: string, text: string[] }[] = [];
  
    constructor(private chatService: ChatService) {}
    
    sendMessage(exampleQuestion?: string): void {
        // get user input query
        const userInput = exampleQuestion ? exampleQuestion.trim() : this.userInput.trim();
        if (!userInput) return;

        this.appendMessage('user', ["User: " + userInput]);
        this.isThinking = true;
        this.userInput = '';
        const messagePayload = {
            userQuery: userInput,
            modelSelection: this.modelSelection,
            currentSummary: this.currentSummary };

        this.chatService.sendMessage(messagePayload).subscribe({
            next: data => {
                this.isThinking = false;
                let res: string[] = [];
                // iterate across agent responses (indices 0 & 1)
                for (let i = 0; i < data.length - 1; i ++ ) {
                    let urls: string = "<i>Sources:<i><br>"
                    if (data[i].urls && data[i].urls.length > 0) {
                        // URLs exist, construct the links
                        urls += data[i].urls.map((url: string) => `<a href="${url}" target="_blank">${url}</a><br>`).join('');
                    } else {
                        urls = "<i>Sources not available.<i>";
                    }                                 
                    const message: string = `${data[i].agentName}:<br>${data[i].agentResponse}<br><br>${urls}`;
                    res.push(message);
                }
                // store current summary and append message to UI
                this.currentSummary = data[data.length - 1];
                this.appendMessage("chat", res);
            },
            error: error => {
                console.error('Error fetching chatbot response:', error);
                let errorString: string = "I'm sorry, I'm experiencing technical difficulties right now. Please try again."
                this.appendMessage("chat", [errorString])
                this.isThinking = false;
            },
      });
    }

    // append message to UI
    appendMessage(sender: string, text: string[]) {
        console.log(text);
        this.messages.push({ sender, text });
    }

    // expand text input box dynamically during user typing
    onTextareaInput(event: Event): void {
        const textarea = event.target as HTMLTextAreaElement;
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
    }

    // update modelSelection based on radio button change
    updateModelSelection(event: any) {
        this.modelSelection = event.target.value;
    }

    // clear message history for new chat
    newChat(): void {
        this.isThinking = false;
        this.messages = [];
    }
}
