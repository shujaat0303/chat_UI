import './App.css';
import Prompt from './components/Prompt';
import Speech from './components/Speech';
import { useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (userMessage) => {
    // Add the user's message to the state first
    setMessages((prevMessages) => [...prevMessages, { role: 'user', content: userMessage }]);

    try {
      // Send POST request to Flask API
      const response = await fetch('http://localhost:5000/api/prompt_bot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: messages,
          prompt: userMessage
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        // Add the chatbot's response to the state
        setMessages(data.messages);
      } else {
        console.error('Error in API response:', response.statusText);
      }
    } catch (error) {
      console.error('Error while sending prompt to the bot:', error);
    }
  };

  return (
    <div className="App">
      <div className="conversation px-4">
        {messages.map((message, index) => (
          <Speech key={index} message={message.content} role={message.role} />
        ))}
      </div>
      <Prompt onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
