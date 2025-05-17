import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';

const sidebarLinks = [
  { to: "/portfolio", label: "Portfolio Master" },
  { to: "/bots", label: "Bots" },
  { to: "/create", label: "Create New Bot" },
  { to: "/admin", label: "Admin Panel" },
];

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-terminal-bg flex flex-col">
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

      <div className="flex flex-1 max-w-7xl mx-auto w-full">
        {/* Sidebar */}
        <aside className="w-64 bg-card-dark border-r border-terminal-border py-8 px-4 flex flex-col gap-6">
          <nav className="flex flex-col gap-2">
            {sidebarLinks.map(link => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `terminal-button w-full text-left justify-start ${isActive ? 'border-2 border-terminal-accent bg-terminal-hover text-terminal-accent' : ''}`
                }
                end
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 py-8 px-6">
          <div className="terminal-grid rounded-xl p-4 min-h-[70vh]">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout; 