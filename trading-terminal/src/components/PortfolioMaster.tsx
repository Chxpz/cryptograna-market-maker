import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const PortfolioMaster: React.FC = () => {
  // Placeholder data
  const totalBalance = '$12,500.00';
  const totalProfit = '+$1,200.00';
  const bots = [
    { name: 'SOL/USDC', allocated: '$4,000', profit: '+$400', status: 'Active' },
    { name: 'BTC/SOL', allocated: '$3,500', profit: '+$300', status: 'Active' },
    { name: 'ETH/USDC', allocated: '$5,000', profit: '+$500', status: 'Active' },
  ];

  // Mock performance data (PnL over time)
  const performanceData = [
    { time: '09:00', pnl: 0 },
    { time: '10:00', pnl: 100 },
    { time: '11:00', pnl: 250 },
    { time: '12:00', pnl: 200 },
    { time: '13:00', pnl: 400 },
    { time: '14:00', pnl: 350 },
    { time: '15:00', pnl: 500 },
    { time: '16:00', pnl: 600 },
    { time: '17:00', pnl: 1200 },
  ];

  // Mock win/loss data
  const winCount = 68;
  const lossCount = 32;
  const winLossData = [
    { name: 'Wins', value: winCount },
    { name: 'Losses', value: lossCount },
  ];
  const COLORS = ['#22d3ee', '#f43f5e'];
  const winRate = ((winCount / (winCount + lossCount)) * 100).toFixed(1);
  const lossRate = ((lossCount / (winCount + lossCount)) * 100).toFixed(1);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="terminal-card flex-1">
          <h2 className="text-lg font-bold text-terminal-accent mb-2">Total Balance</h2>
          <p className="text-3xl font-extrabold">{totalBalance}</p>
        </div>
        <div className="terminal-card flex-1">
          <h2 className="text-lg font-bold text-terminal-success mb-2">Total Profit</h2>
          <p className="text-3xl font-extrabold text-terminal-success">{totalProfit}</p>
        </div>
      </div>

      {/* Performance Chart */}
      <div className="terminal-card">
        <h2 className="text-lg font-bold text-terminal-accent mb-4">Performance (PnL Over Time)</h2>
        <div className="h-64">
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

      {/* Win/Loss Summary */}
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
          <h2 className="text-lg font-bold text-terminal-accent mb-4">Bot Allocation</h2>
          <table className="terminal-table">
            <thead>
              <tr>
                <th>Bot</th>
                <th>Allocated</th>
                <th>Profit</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {bots.map((bot, idx) => (
                <tr key={idx}>
                  <td>{bot.name}</td>
                  <td>{bot.allocated}</td>
                  <td className="text-terminal-success">{bot.profit}</td>
                  <td>
                    <span className="terminal-badge terminal-badge-success">{bot.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default PortfolioMaster; 