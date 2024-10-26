import Markdown from 'react-markdown'


function Speech({ message, role }) {
  return (
    <div className={`speech-bubble-area my-2 ${role === 'user' ? 'user-bubble' : 'bot-bubble'}`}>
      <div className={`speech-bubble px-3 py-2 ${role === 'user' ? 'align-right' : 'align-left'}`}>
        <p><Markdown>{message}</Markdown></p>
      </div>
    </div>
  );
}

export default Speech;
