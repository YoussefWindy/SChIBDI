const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', async () => {
    const message = userInput.value;
    if (message.trim() === '') return;

    appendMessage('You: ' + message);
    userInput.value = '';

    const response = await sendMessageToChatbot(message);
    appendMessage('Bot: ' + response);
});

async function sendMessageToChatbot(message) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });

    if (!response.ok) {
        console.error('Error:', response.statusText);
        return 'Sorry, there was an error.';
    }

    const data = await response.json();
    return data.reply;
}

function appendMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}