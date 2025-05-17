# Cryptograna Market Maker

A high-performance, extensible market making and portfolio management system for decentralized exchanges (DEXes). The first implementation targets Solana, but the architecture is designed to support EVM and other networks in the future.

## AI Agent Architecture

Each bot in Cryptograna is an **AI Agent** (Retrieval-Augmented Generation, RAG) trained to operate as a market maker and portfolio manager. Multiple agents can be deployed simultaneously, each managing its own strategy, trading pair, and resource allocation.

### Agent Capabilities
- **Autonomous Decision-Making:** Each agent can independently analyze market conditions, adjust parameters, and execute trades.
- **Portfolio Management:** Agents manage their allocated resources and report profits back to the master portfolio.
- **Multi-Agent Deployment:** The system supports running multiple agents in parallel, each with its own configuration and trading logic.

### Data Available to Each Agent
Agents have access to the following data for decision-making:
- **Real-Time Market Data:** Order books, trades, and price feeds from integrated DEXes (e.g., Helius, Jupiter, Orca on Solana; EVM DEXes in the future).
- **Portfolio State:** Current allocation, available balance, and historical performance for both the master portfolio and the agent's own allocation.
- **Bot Configuration:** Trading pair, pool address, update interval, risk parameters, and any user-provided notes or constraints.
- **System Metrics:** Latency, error rates, and health status from the monitoring subsystem.
- **Historical Trades:** Full trade history, PnL, and win/loss statistics for the agent and the global system.
- **User/Strategy Inputs:** Manual overrides, special instructions, or AI-guided parameter changes via the dashboard or chat interface.

Agents use this data to:
- Identify trading opportunities
- Adjust spreads, order sizes, and risk parameters
- Rebalance or reallocate funds
- Pause, stop, or escalate issues based on system health or user intervention

The AI Agent framework is designed to be extensible, allowing for future integration of new data sources, advanced strategies, and cross-chain operation.

## Features

### Core Components
- **Market Data Collector**: Real-time data collection from multiple sources with validation and rate limiting
- **Trading Strategy**: Pure market making with dynamic parameter adjustment
- **Hummingbot Controller**: Order execution and parameter management
- **Monitoring System**: Prometheus metrics and Grafana dashboards
- **Unified Portfolio Master**: Centralized resource allocation and profit routing
- **Bot Management**: Create, pause, stop, edit, and monitor bots for any supported network
- **AI Agent**: Conversational bot creation and management

### Key Features
- Real-time market data collection (Helius, Jupiter, Orca, and more)
- Dynamic spread and order size calculation
- Position tracking and risk management
- Circuit breakers for drawdown protection
- Comprehensive monitoring and metrics
- Automated error recovery
- Rate limiting and caching
- Multi-network extensibility (Solana-first, EVM-ready)

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Hummingbot instance
- Node.js 18+
- API keys for:
  - Helius
  - Jupiter
  - Orca

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chxpz/cryptograna-market-maker.git
cd cryptograna-market-maker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The bot is configured through environment variables. Key settings include:

### API Keys
- `HELIUS_API_KEY`: Your Helius API key
- `JUPITER_API_KEY`: Your Jupiter API key
- `ORCA_API_KEY`: Your Orca API key

### Trading Parameters
- `MIN_SPREAD`: Minimum spread percentage
- `MAX_SPREAD`: Maximum spread percentage
- `ORDER_SIZE`: Base order size
- `MAX_POSITION_SIZE`: Maximum position size
- `UPDATE_INTERVAL`: Strategy update interval in seconds

### Risk Parameters
- `MAX_DRAWDOWN`: Maximum allowed drawdown
- `STOP_LOSS`: Stop loss percentage
- `MAX_LEVERAGE`: Maximum leverage

### Monitoring
- `PROMETHEUS_PORT`: Port for Prometheus metrics
- `METRICS_UPDATE_INTERVAL`: Metrics update interval
- `LOG_LEVEL`: Logging level

## Usage

1. Start the bot:
```bash
./scripts/run_bot.sh
```

2. Monitor performance:
- View logs in the `logs/` directory
- Access Grafana dashboard at http://localhost:3000
- View Prometheus metrics at http://localhost:9090

## Architecture Overview

- **Portfolio Master**: Controls balance, allocation, profit routing, and withdrawals.
- **Bots**: Independent instances, each with its own config and allocated resources.
- **Decision Module**: AI/algorithm that selects assets, adjusts parameters, and reallocates resources.
- **User Interface**: Dashboard for monitoring, bot creation, and portfolio overview.
- **BFF (Backend for Frontend)**: Single API layer for all frontend/backend communication.

## Example Use Cases
- Run the system fully autonomously, only withdrawing profits periodically.
- Manually create a bot for a new promising pair, allocating part of the master portfolio.
- Monitor the performance of each bot and the overall portfolio in real time.

# API Documentation

All frontend/backend communication is handled via the BFF API. Below are the endpoints, methods, parameters, and expected responses.

## System Settings
- **GET /admin/settings**
  - Returns: `SystemSettings`
  - Description: Get current system settings (limits, intervals, risk, etc)
- **PUT /admin/settings**
  - Body: `SystemSettings`
  - Returns: 200 OK
  - Description: Update system settings

## System Logs
- **GET /admin/logs**
  - Returns: `SystemLog[]`
  - Description: Get recent system logs
- **POST /admin/logs/clear**
  - Returns: 200 OK
  - Description: Clear all system logs

## Fund Management
- **GET /admin/funds/summary**
  - Returns: `FundSummary`
  - Description: Get total, available, and allocated funds
- **GET /admin/funds/transactions**
  - Returns: `FundTransaction[]`
  - Description: Get recent fund transactions
- **POST /admin/funds/deposit**
  - Body: `{ amount: number }`
  - Returns: 200 OK
  - Description: Deposit funds into the system
- **POST /admin/funds/withdraw**
  - Body: `{ amount: number }`
  - Returns: 200 OK
  - Description: Withdraw funds from the system
- **POST /admin/funds/transfer**
  - Body: `{ from: string, to: string, amount: number }`
  - Returns: 200 OK
  - Description: Transfer funds between bots or accounts

## Types
- `SystemSettings`: `{ maxBots: number, maxAllocationPerBot: number, updateInterval: number, riskLevel: 'low'|'medium'|'high', autoReinvest: boolean, emergencyStop: boolean }`
- `SystemLog`: `{ timestamp: string, level: 'info'|'warning'|'error', message: string }`
- `FundSummary`: `{ totalBalance: number, availableFunds: number, allocatedFunds: number }`
- `FundTransaction`: `{ id: string, timestamp: string, type: 'deposit'|'withdrawal'|'transfer', amount: number, status: 'pending'|'completed'|'failed', from: string, to: string }`

# Technical Roadmap & TODO

This section tracks the remaining work to bring the Cryptograna Market Maker system to full production readiness. Update as the project evolves.

---

## 1. Backend for Frontend (BFF) Implementation
- [ ] Implement a BFF service (Node.js/Express, FastAPI, or similar) that exposes all endpoints needed by the frontend.
- [ ] BFF should aggregate, validate, and format data from the core backend, bots, and portfolio modules.
- [ ] Add authentication and authorization middleware.
- [ ] Provide mock endpoints for local frontend development.

## 2. Core Backend Modules
- [ ] Portfolio Master: resource allocation, profit routing, withdrawals.
- [ ] Bot Management: create, pause, stop, edit, remove bots; track status and config.
- [ ] Trade Execution: connect to Hummingbot, manage orders, handle errors.
- [ ] Analytics: PnL, win/loss, trade history, per-bot and global.
- [ ] Logging & Auditing: system logs, user actions, error tracking.
- [ ] Fund Management: deposits, withdrawals, transfers, transaction history.

## 3. AI Agent Integration
- [ ] Implement backend logic for the AI agent (bot creation, Q&A, troubleshooting).
- [ ] Connect frontend chat terminals to real AI agent endpoints.
- [ ] Add context awareness and memory to the agent for multi-step flows.

## 4. Admin & Security
- [ ] Complete Admin Panel: system settings, logs, fund management, user management.
- [ ] Add authentication (JWT, OAuth, etc.) and role-based access control.
- [ ] Implement audit trails for all admin/user actions.

## 5. Testing & Quality Assurance
- [ ] Add unit and integration tests for all backend modules.
- [ ] Add frontend tests (React Testing Library, Cypress, etc.).
- [ ] End-to-end tests for critical user flows.

---

_This section is the source of truth for project progress. Update as you complete or add new features._
