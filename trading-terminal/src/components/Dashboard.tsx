import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data for the chart
const performanceData = [
  { time: '00:00', pnl: 0 },
  { time: '01:00', pnl: 100 },
  { time: '02:00', pnl: 150 },
  { time: '03:00', pnl: 120 },
  { time: '04:00', pnl: 200 },
  { time: '05:00', pnl: 180 },
  { time: '06:00', pnl: 250 },
];

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-4">
      {/* Trading Metrics */}
      <div className="grid grid-cols-4 gap-4">
        <div className="terminal-card terminal-glow">
          <h3 className="text-sm text-gray-400">Total PnL</h3>
          <p className="text-2xl font-bold text-terminal-success">+$1,234.56</p>
          <p className="text-sm text-terminal-success">+2.34%</p>
        </div>
        <div className="terminal-card terminal-glow">
          <h3 className="text-sm text-gray-400">Position Size</h3>
          <p className="text-2xl font-bold">123.45 SOL</p>
          <p className="text-sm text-gray-400">≈ $12,345.67</p>
        </div>
        <div className="terminal-card terminal-glow">
          <h3 className="text-sm text-gray-400">24h Volume</h3>
          <p className="text-2xl font-bold">$45,678.90</p>
          <p className="text-sm text-gray-400">123 trades</p>
        </div>
        <div className="terminal-card terminal-glow">
          <h3 className="text-sm text-gray-400">Win Rate</h3>
          <p className="text-2xl font-bold text-terminal-success">68.5%</p>
          <p className="text-sm text-gray-400">Last 100 trades</p>
        </div>
      </div>

      {/* Performance Chart */}
      <div className="terminal-card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-terminal-accent">Performance</h2>
          <div className="flex space-x-2">
            <button className="terminal-button text-sm">1H</button>
            <button className="terminal-button text-sm">24H</button>
            <button className="terminal-button text-sm">7D</button>
          </div>
        </div>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={performanceData}>
              <defs>
                <linearGradient id="colorPnl" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00f2fe" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#00f2fe" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#111827',
                  border: '1px solid #1f2937',
                  borderRadius: '0.375rem',
                  color: '#e2e8f0',
                }}
              />
              <Line
                type="monotone"
                dataKey="pnl"
                stroke="#00f2fe"
                strokeWidth={2}
                dot={false}
                fill="url(#colorPnl)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Trades */}
      <div className="terminal-card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-terminal-accent">Recent Trades</h2>
          <button className="terminal-button text-sm">View All</button>
        </div>
        <div className="overflow-x-auto">
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
              <tr>
                <td>2024-02-17 20:30:15</td>
                <td><span className="text-terminal-success">BUY</span></td>
                <td>$98.45</td>
                <td>1.23 SOL</td>
                <td>$121.09</td>
                <td><span className="terminal-badge terminal-badge-success">Filled</span></td>
              </tr>
              <tr>
                <td>2024-02-17 20:25:30</td>
                <td><span className="text-terminal-error">SELL</span></td>
                <td>$98.75</td>
                <td>0.85 SOL</td>
                <td>$83.94</td>
                <td><span className="terminal-badge terminal-badge-success">Filled</span></td>
              </tr>
              <tr>
                <td>2024-02-17 20:20:45</td>
                <td><span className="text-terminal-success">BUY</span></td>
                <td>$98.30</td>
                <td>2.15 SOL</td>
                <td>$211.35</td>
                <td><span className="terminal-badge terminal-badge-warning">Partial</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 