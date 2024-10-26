import { useState } from 'react';

function Prompt({ onSendMessage }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);  // Send the user's input to the parent component (App.js)
      setInput('');  // Clear the input field after submitting
    }
  };

  return (
    <form onSubmit={handleSubmit} className='prompt-container input-group input-group-lg'>
      <input 
        className='prompt input my-2 px-3'
        type='text' 
        placeholder='Ask the Chatbot'
        value={input}
        onChange={(e) => setInput(e.target.value)}  // Update input state
      />
      <button className='btn btn-primary prompt-submit my-2' type='submit'>
        Send
      </button>
    </form>
  );
}

export default Prompt;
