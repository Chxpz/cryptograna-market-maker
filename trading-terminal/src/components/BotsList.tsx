import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const BotsList: React.FC = () => {
  const navigate = useNavigate();
  const [tab, setTab] = useState<'active' | 'inactive'>('active');

  // Mock data
  const activeBots = [
    { name: 'SOL/USDC', pair: 'SOL/USDC', allocated: '$4,000', profit: '+$400', status: 'Active', since: '2024-05-01' },
    { name: 'BTC/SOL', pair: 'BTC/SOL', allocated: '$3,500', profit: '+$300', status: 'Active', since: '2024-05-03' },
    { name: 'ETH/USDC', pair: 'ETH/USDC', allocated: '$5,000', profit: '+$500', status: 'Active', since: '2024-05-05' },
  ];
  const inactiveBots = [
    { name: 'SOL/USDT', pair: 'SOL/USDT', allocated: '$2,000', profit: '+$150', status: 'Stopped', since: '2024-04-10' },
    { name: 'BTC/USDC', pair: 'BTC/USDC', allocated: '$1,500', profit: '-$50', status: 'Paused', since: '2024-03-22' },
    { name: 'ETH/BTC', pair: 'ETH/BTC', allocated: '$2,200', profit: '+$80', status: 'Removed', since: '2024-02-15' },
  ];

  const bots = tab === 'active' ? activeBots : inactiveBots;

  const statusBadgeClass = (status: string) => {
    if (status === 'Active') return 'terminal-badge terminal-badge-success';
    if (status === 'Paused') return 'terminal-badge terminal-badge-warning';
    if (status === 'Stopped') return 'terminal-badge terminal-badge-error';
    if (status === 'Removed') return 'terminal-badge';
    return 'terminal-badge';
  };

  const handleRowClick = (bot: typeof bots[0]) => {
    navigate(`/bots/${encodeURIComponent(bot.name)}`);
  };

  return (
    <div className="terminal-card">
      <div className="flex gap-4 mb-4">
        <button
          className={`px-4 py-2 rounded-xl font-bold ${tab === 'active' ? 'bg-terminal-accent text-white' : 'bg-button-dark text-terminal-fg'}`}
          onClick={() => setTab('active')}
        >
          Active Bots
        </button>
        <button
          className={`px-4 py-2 rounded-xl font-bold ${tab === 'inactive' ? 'bg-terminal-accent text-white' : 'bg-button-dark text-terminal-fg'}`}
          onClick={() => setTab('inactive')}
        >
          Inactive Bots
        </button>
      </div>
      <table className="terminal-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Pair</th>
            <th>Allocated</th>
            <th>Profit</th>
            <th>Status</th>
            <th>Since</th>
          </tr>
        </thead>
        <tbody>
          {bots.map((bot, idx) => (
            <tr
              key={idx}
              className="cursor-pointer hover:bg-terminal-hover transition-colors"
              onClick={() => handleRowClick(bot)}
            >
              <td>{bot.name}</td>
              <td>{bot.pair}</td>
              <td>{bot.allocated}</td>
              <td className={bot.profit.startsWith('+') ? 'text-terminal-success' : 'text-terminal-error'}>{bot.profit}</td>
              <td>
                <span className={statusBadgeClass(bot.status)}>{bot.status}</span>
              </td>
              <td>{bot.since}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BotsList; 