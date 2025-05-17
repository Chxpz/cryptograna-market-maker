/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'terminal-bg': '#151924',
        'terminal-fg': '#e5e7eb',
        'terminal-accent': '#3b82f6',
        'terminal-accent-secondary': '#6366f1',
        'terminal-success': '#22d3ee',
        'terminal-warning': '#fbbf24',
        'terminal-error': '#f43f5e',
        'terminal-border': '#23263a',
        'terminal-hover': '#23263a',
        'button-dark': '#23263a',
        'button-dark-hover': '#334155',
        'card-dark': '#1a1d2a',
        'terminal-card': '#1a1d2a',
        'terminal-input': '#23263a',
        'terminal-grid': '#23263a',
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      boxShadow: {
        'soft': '0 2px 8px 0 rgba(59, 130, 246, 0.08)',
        'card': '0 2px 16px 0 rgba(0,0,0,0.12)',
      },
      borderRadius: {
        'xl': '1rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} 