import { Component, AfterViewChecked, ViewChild, ElementRef } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ChatService } from './chat.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [RouterModule, FormsModule, CommonModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements AfterViewChecked {
    userInput: string = '';
    modelSelection: string = 'both';
    currentSummary: string = '';
    isThinking: boolean = false;
    messages: { sender: string, text: string[] }[] = [];

    @ViewChild('chatArea') private chatArea!: ElementRef;

    constructor(private chatService: ChatService) {}

    sendMessage(exampleQuestion?: string): void {
        const userInput = exampleQuestion ? exampleQuestion.trim() : this.userInput.trim();
        if (!userInput) return;

        this.appendMessage('user', ["User: " + userInput]);
        this.isThinking = true;
        this.userInput = '';
        const messagePayload = {
            userQuery: userInput,
            modelSelection: this.modelSelection,
            currentSummary: this.currentSummary 
        };

        this.chatService.sendMessage(messagePayload).subscribe({
            next: data => {
                this.isThinking = false;
                let res: string[] = [];
                for (let i = 0; i < data.length - 1; i++) {
                    let urls: string = "<i>Sources:<i><br>";
                    if (data[i].urls && data[i].urls.length > 0) {
                        urls += data[i].urls.map((url: string) => `<a href="${url}" target="_blank">${url}</a><br>`).join('');
                    } else {
                        urls = "<i>Sources not available.<i>";
                    }                                 
                    const message: string = `${data[i].agentName}:<br>${data[i].agentResponse}<br><br>${urls}`;
                    res.push(message);
                }
                this.currentSummary = data[data.length - 1];
                this.appendMessage("chat", res);
            },
            error: error => {
                console.error('Error fetching chatbot response:', error);
                let errorString: string = "I'm sorry, I'm experiencing technical difficulties right now. Please try again.";
                this.appendMessage("chat", [errorString]);
                this.isThinking = false;
            },
        });
    }

    appendMessage(sender: string, text: string[]) {
        this.messages.push({ sender, text });
        this.scrollToBottom(); // Scroll to the bottom after a new message is added
    }

    onTextareaInput(event: Event): void {
        const textarea = event.target as HTMLTextAreaElement;
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
    }

    updateModelSelection(event: any) {
        this.modelSelection = event.target.value;
    }

    newChat(): void {
        this.isThinking = false;
        this.messages = [];
    }

    scrollToBottom(): void {
        try {
            if (this.chatArea) {
                this.chatArea.nativeElement.scrollTop = this.chatArea.nativeElement.scrollHeight;
            }
        } catch (err) {
            console.error('Error scrolling to bottom:', err);
        }
    }

    ngAfterViewChecked() {
        this.scrollToBottom();
    }
}
