// This file contains JavaScript code for the frontend, handling client-side interactions and DOM manipulation.

document.addEventListener('DOMContentLoaded', function() {
    const greetingElement = document.getElementById('greeting');
    greetingElement.textContent = 'Welcome to My Web App!';

    const button = document.getElementById('myButton');
    button.addEventListener('click', function() {
        alert('Button clicked!');
    });
});