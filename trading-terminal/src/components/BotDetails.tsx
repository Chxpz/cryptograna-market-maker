import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const BotDetails: React.FC = () => {
  const { botId } = useParams();
  const navigate = useNavigate();

  // Mock bot data (simulate inactive bot if botId includes 'USDT', 'Paused', 'Stopped', or 'Removed')
  const isInactive = botId && (botId.includes('USDT') || botId.includes('Paused') || botId.includes('Stopped') || botId.includes('Removed'));
  const bot = {
    id: botId,
    name: botId,
    pair: botId,
    allocated: isInactive ? '$2,000' : '$4,000',
    profit: isInactive ? '+$150' : '+$400',
    status: isInactive ? (botId?.includes('Paused') ? 'Paused' : botId?.includes('Stopped') ? 'Stopped' : botId?.includes('Removed') ? 'Removed' : 'Stopped') : 'Active',
    config: {
      updateInterval: 30,
      spread: '0.2% - 0.5%',
      poolAddress: '0x123...abc',
    },
    aiName: `${botId} AI Agent`,
    aiAvatar: '🤖',
  };

  // Mock per-bot performance data
  const performanceData = [
    { time: '09:00', pnl: 0 },
    { time: '10:00', pnl: 20 },
    { time: '11:00', pnl: 50 },
    { time: '12:00', pnl: 40 },
    { time: '13:00', pnl: 80 },
    { time: '14:00', pnl: 120 },
    { time: '15:00', pnl: 200 },
    { time: '16:00', pnl: 300 },
    { time: '17:00', pnl: 400 },
  ];

  // Mock win/loss data
  const winCount = 18;
  const lossCount = 7;
  const winLossData = [
    { name: 'Wins', value: winCount },
    { name: 'Losses', value: lossCount },
  ];
  const COLORS = ['#22d3ee', '#f43f5e'];
  const winRate = ((winCount / (winCount + lossCount)) * 100).toFixed(1);
  const lossRate = ((lossCount / (winCount + lossCount)) * 100).toFixed(1);

  // Mock trade history
  const trades = [
    { time: '16:55', type: 'BUY', price: '$98.45', amount: '1.23', total: '$121.09', status: 'Filled' },
    { time: '16:40', type: 'SELL', price: '$98.75', amount: '0.85', total: '$83.94', status: 'Filled' },
    { time: '16:20', type: 'BUY', price: '$98.30', amount: '2.15', total: '$211.35', status: 'Partial' },
  ];

  // Actions (placeholders)
  const handlePause = () => alert('Pause bot (not implemented)');
  const handleStop = () => alert('Stop bot (not implemented)');
  const handleEdit = () => alert('Edit bot (not implemented)');
  const handleRemove = () => {
    if (window.confirm('Are you sure you want to remove this bot?')) {
      alert('Remove bot (not implemented)');
      navigate('/bots');
    }
  };

  // AI Agent Chat State
  const [chat, setChat] = useState([
    { sender: 'bot', text: 'Hello! I am your AI agent for this strategy. Ask me anything about my performance, decisions, or configuration.' },
  ]);
  const [input, setInput] = useState('');
  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    setChat(prev => [
      ...prev,
      { sender: 'user', text: input },
      // Mock bot response
      { sender: 'bot', text: `You asked: "${input}". (This is a mock response.)` },
    ]);
    setInput('');
  };

  return (
    <div className="space-y-6 pb-8">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="terminal-card flex-1">
          <h2 className="text-lg font-bold text-terminal-accent mb-2">Bot Details</h2>
          {isInactive && (
            <div className="mb-3 p-2 rounded bg-terminal-warning bg-opacity-10 text-terminal-warning font-semibold">
              This bot is inactive. Data is read-only and actions are disabled.
            </div>
          )}
          <div className="mb-2"><span className="font-semibold">Pair:</span> {bot.pair}</div>
          <div className="mb-2"><span className="font-semibold">Allocated:</span> {bot.allocated}</div>
          <div className="mb-2"><span className="font-semibold">Profit:</span> <span className="text-terminal-success">{bot.profit}</span></div>
          <div className="mb-2"><span className="font-semibold">Status:</span> <span className={`terminal-badge ${bot.status === 'Active' ? 'terminal-badge-success' : bot.status === 'Paused' ? 'terminal-badge-warning' : bot.status === 'Stopped' ? 'terminal-badge-error' : ''}`}>{bot.status}</span></div>
          <div className="mb-2"><span className="font-semibold">Update Interval:</span> {bot.config.updateInterval}s</div>
          <div className="mb-2"><span className="font-semibold">Spread:</span> {bot.config.spread}</div>
          <div className="mb-2"><span className="font-semibold">Pool Address:</span> <span className="font-mono text-xs">{bot.config.poolAddress}</span></div>
          <div className="flex gap-2 mt-4">
            <button className="terminal-button" onClick={handlePause} disabled={!!isInactive}>Pause</button>
            <button className="terminal-button-danger" onClick={handleStop} disabled={!!isInactive}>Stop</button>
            <button className="terminal-button" onClick={handleEdit} disabled={!!isInactive}>Edit</button>
            <button className="terminal-button-danger" onClick={handleRemove} disabled={!!isInactive}>Remove</button>
          </div>
        </div>
        <div className="terminal-card flex-1">
          <h2 className="text-lg font-bold text-terminal-accent mb-4">Performance (PnL Over Time)</h2>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#23263a" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#1a1d2a', border: '1px solid #23263a', color: '#e5e7eb' }} />
                <Line type="monotone" dataKey="pnl" stroke="#22d3ee" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <div className="flex flex-col md:flex-row gap-6">
        <div className="terminal-card flex-1 flex flex-col items-center justify-center">
          <h2 className="text-lg font-bold text-terminal-accent mb-2">Win/Loss Ratio</h2>
          <div className="flex items-center gap-8 w-full">
            <div className="flex flex-col items-center flex-1">
              <span className="text-2xl font-bold text-terminal-success">{winCount}</span>
              <span className="text-sm text-terminal-success">Wins</span>
              <span className="text-xs text-terminal-fg/60">{winRate}%</span>
            </div>
            <div className="flex flex-col items-center flex-1">
              <span className="text-2xl font-bold text-terminal-error">{lossCount}</span>
              <span className="text-sm text-terminal-error">Losses</span>
              <span className="text-xs text-terminal-fg/60">{lossRate}%</span>
            </div>
            <div className="flex-1">
              <PieChart width={100} height={100}>
                <Pie
                  data={winLossData}
                  cx={50}
                  cy={50}
                  innerRadius={28}
                  outerRadius={40}
                  fill="#8884d8"
                  paddingAngle={2}
                  dataKey="value"
                >
                  {winLossData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Legend verticalAlign="bottom" height={24} iconType="circle" />
              </PieChart>
            </div>
          </div>
        </div>
        <div className="terminal-card flex-1">
          <h2 className="text-lg font-bold text-terminal-accent mb-4">Trade History</h2>
          <table className="terminal-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Type</th>
                <th>Price</th>
                <th>Amount</th>
                <th>Total</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade, idx) => (
                <tr key={idx}>
                  <td>{trade.time}</td>
                  <td className={trade.type === 'BUY' ? 'text-terminal-success' : 'text-terminal-error'}>{trade.type}</td>
                  <td>{trade.price}</td>
                  <td>{trade.amount}</td>
                  <td>{trade.total}</td>
                  <td>
                    <span className={`terminal-badge ${trade.status === 'Filled' ? 'terminal-badge-success' : 'terminal-badge-warning'}`}>{trade.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* AI Agent Chat Terminal (not fixed, at the bottom) */}
      <div className="mt-8">
        <div className="terminal-card max-w-2xl mx-auto border-t-2 border-terminal-border shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-2xl">{bot.aiAvatar}</span>
            <span className="font-bold text-terminal-accent text-lg">{bot.aiName}</span>
          </div>
          <div className="h-40 overflow-y-auto bg-terminal-bg rounded-xl p-3 mb-2 border border-terminal-border" style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.95rem' }}>
            {chat.map((msg, idx) => (
              <div key={idx} className={msg.sender === 'user' ? 'text-terminal-accent text-right mb-2' : 'text-terminal-fg text-left mb-2'}>
                {msg.sender === 'user' ? <span className="font-bold">You: </span> : <span className="font-bold">{bot.aiName}: </span>}
                {msg.text}
              </div>
            ))}
          </div>
          <form className="flex gap-2" onSubmit={handleChatSubmit}>
            <input
              className="terminal-input flex-1"
              type="text"
              placeholder="Ask the AI agent anything..."
              value={input}
              onChange={e => setInput(e.target.value)}
            />
            <button className="terminal-button" type="submit">Send</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default BotDetails; 