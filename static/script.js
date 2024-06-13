// script.js

const chatBox = document.getElementById('chat-box');

async function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput === '') return;

    appendMessage('user', userInput);
    document.getElementById('user-input').value = '';

    try {
        document.getElementById('typing-dots').style.display = 'inline-block';

        const response = await fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch response from the server');
        }

        const data = await response.json();
        appendMessage('chatbot', data.response);
        console.log('Chatbot response:', data.response); // Debugging output
    } catch (error) {
        console.error('Error fetching chatbot response:', error);
        // Handle the error (e.g., display an error message to the user)
    } finally {
        document.getElementById('typing-dots').style.display = 'none';
    }
}

function appendMessage(role, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', role === 'user' ? 'user-message' : 'chatbot-message');

    const label = document.createElement('span');
    label.textContent = role === 'user' ? 'You: ' : 'MediChat: ';
    label.style.fontWeight = 'bold';
    messageElement.appendChild(label);

    const content = document.createElement('span');
    content.textContent = message;
    content.style.overflowWrap = 'break-word';
    messageElement.appendChild(content);

    chatBox.appendChild(messageElement);

    // Add a line break after each message
    chatBox.appendChild(document.createElement('br'));
    chatBox.appendChild(document.createElement('br'));

    chatBox.scrollTop = chatBox.scrollHeight;
}


document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Event listener for "Enter" key press
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            // Hide the divs with classes "ex", "greeting", and "greeting1"
            document.querySelector('.ex').style.display = 'none';
            document.querySelector('.greeting').style.display = 'none';
            document.querySelector('.greeting1').style.display = 'none';
        }
    });

    document.getElementById('send-btn').addEventListener('click', function() {
        // Show the divs with classes "ex", "greeting", and "greeting1"
        document.querySelector('.ex').style.display = 'none';
        document.querySelector('.greeting').style.display = 'none';
        document.querySelector('.greeting1').style.display = 'none';

    });

    // Event listener for "new chat" button click
    document.getElementById('new-chat-btn').addEventListener('click', async function() {
        // Archive the current conversation
        await archiveConversation();
    
        // Show the divs with classes "ex", "greeting", and "greeting1"
        document.querySelector('.ex').style.display = 'flex';
        document.querySelector('.greeting').style.display = 'block';
        document.querySelector('.greeting1').style.display = 'block';
    
        // Clear the chat box
        document.getElementById('chat-box').innerHTML = '';
    });
    
    async function archiveConversation() {
        // Extract the current chat messages from the chat box
        const messages = [];
        document.querySelectorAll('.message').forEach(message => {
            const role = message.classList.contains('user-message') ? 'user' : 'chatbot';
            const content = message.querySelector('span').textContent;
            messages.push({ role, content });
        });
    
        // Send an AJAX request to the server to archive the conversation
        try {
            const response = await fetch('/archive_conversation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ messages })
            });
    
            if (!response.ok) {
                throw new Error('Failed to archive conversation');
            }
    
            console.log('Conversation archived successfully');
        } catch (error) {
            console.error('Error archiving conversation:', error);
        }
    }
    
});
