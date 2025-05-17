import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-terminal-bg">
      {/* Top Navigation */}
      <nav className="bg-card-dark border-b border-terminal-border backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20 items-center">
            <div className="flex flex-col justify-center">
              <span className="text-2xl font-extrabold bg-gradient-to-r from-terminal-accent via-terminal-accent-secondary to-terminal-success bg-clip-text text-transparent drop-shadow-lg tracking-tight">
                Cryptograna Market Maker&apos;s Dashboard
              </span>
              <span className="text-sm text-terminal-fg/70 mt-1 font-mono italic">Profit never sleeps. Neither do we. 🚀</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="terminal-badge terminal-badge-success">System Online</span>
              <span className="text-sm text-terminal-fg/60">v0.1.0</span>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-12 gap-4">
          {/* Left Sidebar */}
          <div className="col-span-3">
            <div className="terminal-card space-y-4">
              <h2 className="text-lg font-semibold text-terminal-accent">Trading Pairs</h2>
              <div className="space-y-2">
                <NavLink
                  to="/"
                  className={({ isActive }) =>
                    `terminal-button w-full flex items-center justify-between ${
                      isActive ? 'border-terminal-accent' : ''
                    }`
                  }
                >
                  <span>SOL/USDC</span>
                  <span className="text-xs text-terminal-success">+2.34%</span>
                </NavLink>
                <NavLink
                  to="/orderbook"
                  className={({ isActive }) =>
                    `terminal-button w-full flex items-center justify-between ${
                      isActive ? 'border-terminal-accent' : ''
                    }`
                  }
                >
                  <span>SOL/USDT</span>
                  <span className="text-xs text-terminal-error">-0.45%</span>
                </NavLink>
                <NavLink
                  to="/controls"
                  className={({ isActive }) =>
                    `terminal-button w-full flex items-center justify-between ${
                      isActive ? 'border-terminal-accent' : ''
                    }`
                  }
                >
                  <span>BTC/SOL</span>
                  <span className="text-xs text-terminal-success">+1.23%</span>
                </NavLink>
              </div>
            </div>

            {/* System Stats */}
            <div className="terminal-card mt-4">
              <h2 className="text-lg font-semibold text-terminal-accent mb-4">System Stats</h2>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-terminal-fg/60">CPU Usage</span>
                  <span className="text-sm">32%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-terminal-fg/60">Memory</span>
                  <span className="text-sm">1.2GB</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-terminal-fg/60">Uptime</span>
                  <span className="text-sm">2d 4h 15m</span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="col-span-9">
            <div className="terminal-grid rounded-xl p-4">
              <Outlet />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Layout; 