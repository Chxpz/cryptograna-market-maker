import React, { useState } from 'react';

const BotControls: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [parameters, setParameters] = useState({
    minSpread: 0.1,
    maxSpread: 0.5,
    orderSize: 1.0,
    maxPositionSize: 100,
    updateInterval: 30,
  });

  const handleParameterChange = (param: string, value: string) => {
    setParameters(prev => ({
      ...prev,
      [param]: parseFloat(value)
    }));
  };

  return (
    <div className="terminal-card">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-terminal-accent">Bot Controls</h2>
        <button
          className={`terminal-button ${isRunning ? 'terminal-button-danger' : ''}`}
          onClick={() => setIsRunning(!isRunning)}
        >
          {isRunning ? 'Stop Bot' : 'Start Bot'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Strategy Parameters */}
        <div className="terminal-card terminal-glow">
          <h3 className="text-sm font-medium text-terminal-accent mb-4">Strategy Parameters</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Min Spread (%)</label>
              <input
                type="number"
                className="terminal-input w-full"
                value={parameters.minSpread}
                onChange={(e) => handleParameterChange('minSpread', e.target.value)}
                step="0.1"
                min="0"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Max Spread (%)</label>
              <input
                type="number"
                className="terminal-input w-full"
                value={parameters.maxSpread}
                onChange={(e) => handleParameterChange('maxSpread', e.target.value)}
                step="0.1"
                min="0"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Order Size (SOL)</label>
              <input
                type="number"
                className="terminal-input w-full"
                value={parameters.orderSize}
                onChange={(e) => handleParameterChange('orderSize', e.target.value)}
                step="0.1"
                min="0"
              />
            </div>
          </div>
        </div>

        {/* Risk Parameters */}
        <div className="terminal-card terminal-glow">
          <h3 className="text-sm font-medium text-terminal-accent mb-4">Risk Parameters</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Max Position Size (SOL)</label>
              <input
                type="number"
                className="terminal-input w-full"
                value={parameters.maxPositionSize}
                onChange={(e) => handleParameterChange('maxPositionSize', e.target.value)}
                step="1"
                min="0"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Update Interval (s)</label>
              <input
                type="number"
                className="terminal-input w-full"
                value={parameters.updateInterval}
                onChange={(e) => handleParameterChange('updateInterval', e.target.value)}
                step="1"
                min="1"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-6 pt-4 border-t border-terminal-border">
        <h3 className="text-sm font-medium text-terminal-accent mb-4">Quick Actions</h3>
        <div className="flex space-x-2">
          <button className="terminal-button">Cancel All Orders</button>
          <button className="terminal-button">Reset Position</button>
          <button className="terminal-button-danger">Emergency Stop</button>
        </div>
      </div>

      {/* Status Information */}
      <div className="mt-4 pt-4 border-t border-terminal-border">
        <div className="grid grid-cols-3 gap-4">
          <div className="terminal-card terminal-glow">
            <span className="text-sm text-gray-400">Status</span>
            <p className={`text-lg font-semibold ${isRunning ? 'text-terminal-success' : 'text-terminal-error'}`}>
              {isRunning ? 'Running' : 'Stopped'}
            </p>
          </div>
          <div className="terminal-card terminal-glow">
            <span className="text-sm text-gray-400">Last Update</span>
            <p className="text-lg font-semibold">2024-02-17 20:30:15</p>
          </div>
          <div className="terminal-card terminal-glow">
            <span className="text-sm text-gray-400">Health</span>
            <p className="text-lg font-semibold text-terminal-success">Healthy</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BotControls; 