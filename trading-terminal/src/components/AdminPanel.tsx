import React, { useState } from 'react';
import { Tab } from '@headlessui/react';

interface SystemLog {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
}

interface FundTransaction {
  id: string;
  timestamp: string;
  type: 'deposit' | 'withdrawal' | 'transfer';
  amount: number;
  status: 'pending' | 'completed' | 'failed';
  from: string;
  to: string;
}

const AdminPanel: React.FC = () => {
  // Mock data - in real implementation, this would come from your backend
  const [systemSettings, setSystemSettings] = useState({
    maxBots: 10,
    maxAllocationPerBot: 10000,
    updateInterval: 60,
    riskLevel: 'medium',
    autoReinvest: true,
    emergencyStop: false,
  });

  const [logs] = useState<SystemLog[]>([
    { timestamp: '2024-03-20 10:00:00', level: 'info', message: 'System startup complete' },
    { timestamp: '2024-03-20 10:05:00', level: 'warning', message: 'High volatility detected in SOL/USDC' },
    { timestamp: '2024-03-20 10:10:00', level: 'error', message: 'Failed to connect to Solana RPC' },
  ]);

  const [transactions] = useState<FundTransaction[]>([
    { id: '1', timestamp: '2024-03-20 09:00:00', type: 'deposit', amount: 5000, status: 'completed', from: 'User Wallet', to: 'System' },
    { id: '2', timestamp: '2024-03-20 09:30:00', type: 'withdrawal', amount: 2000, status: 'pending', from: 'System', to: 'User Wallet' },
    { id: '3', timestamp: '2024-03-20 10:00:00', type: 'transfer', amount: 1000, status: 'completed', from: 'Bot 1', to: 'Bot 2' },
  ]);

  const handleSettingChange = (key: keyof typeof systemSettings, value: any) => {
    setSystemSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
        <h1 className="text-3xl font-extrabold text-terminal-fg tracking-tight">Admin Panel</h1>
        <div className="flex gap-4">
          <button className="terminal-button terminal-button-warning px-6 py-2 text-base font-semibold">Emergency Stop</button>
          <button className="terminal-button terminal-button-success px-6 py-2 text-base font-semibold">Save Changes</button>
        </div>
      </div>

      <div className="rounded-2xl bg-card-dark/80 border border-terminal-border p-4 shadow-card">
        <Tab.Group>
          <Tab.List className="flex space-x-2 rounded-xl bg-card-dark/80 p-2 mb-6">
            {['System Settings', 'System Logs', 'Fund Management'].map((tab, idx) => (
              <Tab key={tab} className={({ selected }) =>
                `flex-1 rounded-lg py-3 px-6 text-base font-mono font-semibold tracking-wide transition-all duration-200
                outline-none border border-transparent
                ${selected
                  ? 'bg-terminal-accent/10 border-terminal-accent text-terminal-accent shadow-lg'
                  : 'text-terminal-fg/80 hover:bg-terminal-hover hover:text-terminal-accent'}
                `
              }>
                {tab}
              </Tab>
            ))}
          </Tab.List>

          <Tab.Panels>
            {/* System Settings Panel */}
            <Tab.Panel className="rounded-xl bg-card-dark p-8 mb-2 shadow-card">
              <h2 className="text-xl font-bold mb-6 text-terminal-accent">System Settings</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div>
                    <label className="block text-base font-medium text-terminal-fg mb-1">Max Bots</label>
                    <input
                      type="number"
                      value={systemSettings.maxBots}
                      onChange={(e) => handleSettingChange('maxBots', parseInt(e.target.value))}
                      className="terminal-input mt-1 w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-base font-medium text-terminal-fg mb-1">Max Allocation per Bot (USD)</label>
                    <input
                      type="number"
                      value={systemSettings.maxAllocationPerBot}
                      onChange={(e) => handleSettingChange('maxAllocationPerBot', parseInt(e.target.value))}
                      className="terminal-input mt-1 w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-base font-medium text-terminal-fg mb-1">Update Interval (seconds)</label>
                    <input
                      type="number"
                      value={systemSettings.updateInterval}
                      onChange={(e) => handleSettingChange('updateInterval', parseInt(e.target.value))}
                      className="terminal-input mt-1 w-full"
                    />
                  </div>
                </div>
                <div className="space-y-6">
                  <div>
                    <label className="block text-base font-medium text-terminal-fg mb-1">Risk Level</label>
                    <select
                      value={systemSettings.riskLevel}
                      onChange={(e) => handleSettingChange('riskLevel', e.target.value)}
                      className="terminal-input mt-1 w-full"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>
                  <div className="flex items-center space-x-3 mt-4">
                    <input
                      type="checkbox"
                      checked={systemSettings.autoReinvest}
                      onChange={(e) => handleSettingChange('autoReinvest', e.target.checked)}
                      className="terminal-checkbox"
                    />
                    <label className="text-base font-medium text-terminal-fg">Auto Reinvest Profits</label>
                  </div>
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={systemSettings.emergencyStop}
                      onChange={(e) => handleSettingChange('emergencyStop', e.target.checked)}
                      className="terminal-checkbox"
                    />
                    <label className="text-base font-medium text-terminal-fg">Emergency Stop Enabled</label>
                  </div>
                </div>
              </div>
            </Tab.Panel>

            {/* System Logs Panel */}
            <Tab.Panel className="rounded-xl bg-card-dark p-8 mb-2 shadow-card">
              <h2 className="text-xl font-bold mb-6 text-terminal-accent">System Logs</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-terminal-fg">Recent Logs</h3>
                  <button className="terminal-button px-4 py-1">Clear Logs</button>
                </div>
                <div className="h-[320px] overflow-y-auto bg-terminal-bg rounded-lg p-4 border border-terminal-border">
                  {logs.map((log, index) => (
                    <div
                      key={index}
                      className={`mb-3 p-3 rounded-lg font-mono text-sm tracking-tight shadow-sm
                        ${log.level === 'error'
                          ? 'bg-red-900/20 text-red-400'
                          : log.level === 'warning'
                          ? 'bg-yellow-900/20 text-yellow-400'
                          : 'bg-green-900/20 text-green-400'}
                      `}
                    >
                      <span className="font-mono text-xs">{log.timestamp}</span>
                      <span className="mx-2">|</span>
                      <span className="uppercase font-bold">{log.level}</span>
                      <span className="mx-2">|</span>
                      <span>{log.message}</span>
                    </div>
                  ))}
                </div>
              </div>
            </Tab.Panel>

            {/* Fund Management Panel */}
            <Tab.Panel className="rounded-xl bg-card-dark p-8 shadow-card">
              <h2 className="text-xl font-bold mb-6 text-terminal-accent">Fund Management</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                <div className="terminal-card flex flex-col items-start gap-2 p-6">
                  <span className="text-base text-terminal-fg/70 font-mono">Total Balance</span>
                  <span className="text-3xl font-extrabold text-terminal-success font-mono">$25,000.00</span>
                </div>
                <div className="terminal-card flex flex-col items-start gap-2 p-6">
                  <span className="text-base text-terminal-fg/70 font-mono">Available Funds</span>
                  <span className="text-3xl font-extrabold text-terminal-accent font-mono">$15,000.00</span>
                </div>
                <div className="terminal-card flex flex-col items-start gap-2 p-6">
                  <span className="text-base text-terminal-fg/70 font-mono">Allocated Funds</span>
                  <span className="text-3xl font-extrabold text-terminal-warning font-mono">$10,000.00</span>
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-4 mb-8">
                <button className="terminal-button flex-1 py-3 text-base font-semibold">Deposit Funds</button>
                <button className="terminal-button flex-1 py-3 text-base font-semibold">Withdraw Funds</button>
                <button className="terminal-button flex-1 py-3 text-base font-semibold">Transfer Funds</button>
              </div>

              <div className="terminal-card p-6 mt-2">
                <h3 className="text-lg font-semibold text-terminal-fg mb-6">Recent Transactions</h3>
                <div className="overflow-x-auto">
                  <table className="terminal-table">
                    <thead>
                      <tr className="text-left text-base text-terminal-fg/70">
                        <th className="p-3 font-mono">Time</th>
                        <th className="p-3 font-mono">Type</th>
                        <th className="p-3 font-mono">Amount</th>
                        <th className="p-3 font-mono">From</th>
                        <th className="p-3 font-mono">To</th>
                        <th className="p-3 font-mono">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {transactions.map((tx) => (
                        <tr key={tx.id} className="border-t border-terminal-border hover:bg-terminal-hover/40">
                          <td className="p-3 font-mono text-base">{tx.timestamp}</td>
                          <td className="p-3 font-mono text-base capitalize">{tx.type}</td>
                          <td className="p-3 font-mono text-base">${tx.amount.toLocaleString()}</td>
                          <td className="p-3 font-mono text-base">{tx.from}</td>
                          <td className="p-3 font-mono text-base">{tx.to}</td>
                          <td className="p-3">
                            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-mono font-semibold
                              ${tx.status === 'completed' ? 'bg-green-900/20 text-green-400' :
                                tx.status === 'pending' ? 'bg-yellow-900/20 text-yellow-400' :
                                'bg-red-900/20 text-red-400'}`}>
                              {tx.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </Tab.Panel>
          </Tab.Panels>
        </Tab.Group>
      </div>
    </div>
  );
};

export default AdminPanel; 