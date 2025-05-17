import React, { useState } from 'react';

interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
}

interface BotDraft {
  pair: string;
  poolAddress: string;
  allocation: string;
  updateInterval: string;
  notes: string;
}

const CreateBot: React.FC = () => {
  // Chat state
  const [chat, setChat] = useState<ChatMessage[]>([
    { sender: 'bot', text: "Hello! I am your AI agent. Let's create a new bot together. Which trading pair would you like to operate? (e.g. SOL/USDC)" },
  ]);
  const [input, setInput] = useState('');
  // Step state for guided flow
  const [step, setStep] = useState(0);
  const [botDraft, setBotDraft] = useState<BotDraft>({ 
    pair: '', 
    poolAddress: '', 
    allocation: '', 
    updateInterval: '', 
    notes: '' 
  });

  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    let nextStep = step;
    let nextDraft = { ...botDraft };
    let botCreated = false;
    let botSummary = '';
    let botResponse = '';

    // Add user message
    setChat(prev => [...prev, { sender: 'user', text: input }]);

    // Guided flow logic
    if (step === 0) {
      nextDraft.pair = input;
      botResponse = `Great! What is the pool address for ${input}?`;
      nextStep = 1;
    } else if (step === 1) {
      nextDraft.poolAddress = input;
      botResponse = 'How much (USD) would you like to allocate to this bot?';
      nextStep = 2;
    } else if (step === 2) {
      nextDraft.allocation = input;
      botResponse = 'What should be the update interval (in seconds)?';
      nextStep = 3;
    } else if (step === 3) {
      nextDraft.updateInterval = input;
      botResponse = 'Any notes or special instructions? (Type "no" to skip)';
      nextStep = 4;
    } else if (step === 4) {
      nextDraft.notes = input.toLowerCase() === 'no' ? '' : input;
      botCreated = true;
      botSummary = `Bot created!\n\nPair: ${nextDraft.pair}\nPool: ${nextDraft.poolAddress}\nAllocation: $${nextDraft.allocation}\nUpdate Interval: ${nextDraft.updateInterval}s\nNotes: ${nextDraft.notes || 'None'}`;
      botResponse = botSummary;
      nextStep = 5;
    } else {
      botResponse = 'Bot already created. Type "restart" to create another.';
      if (input.toLowerCase() === 'restart') {
        nextStep = 0;
        nextDraft = { pair: '', poolAddress: '', allocation: '', updateInterval: '', notes: '' };
        botResponse = "Let's create a new bot! Which trading pair would you like to operate? (e.g. SOL/USDC)";
      }
    }

    setTimeout(() => {
      setChat(prev => [...prev, { sender: 'bot', text: botResponse }]);
    }, 400);
    setInput('');
    setStep(nextStep);
    setBotDraft(nextDraft);
  };

  return (
    <div className="terminal-card max-w-2xl mx-auto mt-12">
      <div className="flex items-center gap-3 mb-2">
        <span className="text-2xl">🤖</span>
        <span className="font-bold text-terminal-accent text-lg">AI Agent - Bot Creation</span>
      </div>
      <div className="h-64 overflow-y-auto bg-terminal-bg rounded-xl p-3 mb-2 border border-terminal-border" style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.95rem' }}>
        {chat.map((msg, idx) => (
          <div key={idx} className={msg.sender === 'user' ? 'text-terminal-accent text-right mb-2' : 'text-terminal-fg text-left mb-2'}>
            {msg.sender === 'user' ? <span className="font-bold">You: </span> : <span className="font-bold">AI Agent: </span>}
            {msg.text.split('\n').map((line, i) => <span key={i}>{line}<br/></span>)}
          </div>
        ))}
      </div>
      <form className="flex gap-2" onSubmit={handleChatSubmit}>
        <input
          className="terminal-input flex-1"
          type="text"
          placeholder={step === 0 ? 'e.g. SOL/USDC' : 'Type your answer...'}
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={step === 5 && input.toLowerCase() !== 'restart'}
        />
        <button className="terminal-button" type="submit" disabled={step === 5 && input.toLowerCase() !== 'restart'}>Send</button>
      </form>
    </div>
  );
};

export default CreateBot; 