# Market Making Bot

A market making bot for Solana DEXes that uses Hummingbot for order execution.

## Features

- Real-time market data collection from multiple sources
- Pure market making strategy with dynamic parameter adjustment
- Risk management and position tracking
- Performance monitoring and metrics
- Docker-based deployment
- Grafana dashboards for visualization

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- API keys for:
  - Helius
  - Jupiter
  - Orca
  - Hummingbot

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd market-making-bot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

4. Run the initialization script:
```bash
./scripts/init.sh
```

## Running the Bot

1. Start the bot:
```bash
./scripts/run_bot.sh
```

2. Monitor the bot:
- Logs are stored in `logs/`
- Grafana dashboard: http://localhost:3000
- Prometheus metrics: http://localhost:9090

## Testing

Run the test suite:
```bash
pytest tests/
```

## Configuration

Key configuration parameters in `.env`:

- `UPDATE_INTERVAL`: Time between strategy updates (seconds)
- `MAX_POSITION_SIZE`: Maximum position size in base currency
- `MIN_SPREAD`: Minimum spread for orders
- `MAX_SPREAD`: Maximum spread for orders
- `TARGET_BASE_PCT`: Target base currency percentage
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## Architecture

The bot consists of several components:

1. **Market Data Collector**: Collects real-time market data from various sources
2. **Trading Strategy**: Implements the market making logic
3. **Hummingbot Controller**: Manages order execution through Hummingbot
4. **Monitoring**: Prometheus metrics and Grafana dashboards

## Roadmap

### Completed
- Project structure and organization
- Environment configuration and setup
- Core components implementation:
  - Market Data Collector with data validation and rate limiting
  - Trading Strategy with market making logic
  - Main trading loop with error handling
  - Basic monitoring setup
- Docker infrastructure
- Basic test suite
- Documentation

### In Progress
- Enhanced monitoring and alerting
  - Custom Grafana dashboards
  - Alert rules for critical events
  - Performance metrics visualization
- Advanced risk management
  - Dynamic position sizing
  - Volatility-based spread adjustment
  - Drawdown protection
- System reliability
  - Automated recovery procedures
  - Health check endpoints
  - Circuit breakers

### Upcoming
- Additional trading strategies
  - Grid trading
  - Mean reversion
  - Statistical arbitrage
- Advanced analytics
  - Market regime detection
  - Liquidity analysis
  - Order flow analysis
- Performance optimization
  - Caching improvements
  - Query optimization
  - Resource utilization
- Security enhancements
  - API key rotation
  - Access control
  - Audit logging

### Future Considerations
- Machine learning integration
  - Price prediction models
  - Market regime classification
  - Risk assessment
- Multi-exchange support
  - Cross-exchange arbitrage
  - Liquidity aggregation
  - Smart order routing
- Community features
  - Strategy marketplace
  - Performance sharing
  - Community metrics
- Enterprise features
  - Multi-account support
  - Advanced reporting
  - Compliance tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

# API Keys
HELIUS_API_KEY=your_helius_api_key
JUPITER_API_KEY=your_jupiter_api_key
ORCA_API_KEY=your_orca_api_key
HUMMINGBOT_URL=http://localhost:9000
HUMMINGBOT_API_KEY=your_hummingbot_api_key

# Trading Parameters
UPDATE_INTERVAL=30
MAX_POSITION_SIZE=100
MIN_SPREAD=0.001
MAX_SPREAD=0.05
TARGET_BASE_PCT=0.5
ORDER_REFRESH_TIME=60
ORDER_AMOUNT=1.0

# Risk Parameters
MAX_DRAWDOWN=0.1
MAX_LEVERAGE=1.0
MIN_LIQUIDITY=10000
STOP_LOSS_PCT=0.02
TAKE_PROFIT_PCT=0.03

# Monitoring
LOG_LEVEL=INFO
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
METRICS_UPDATE_INTERVAL=15

# Cache Settings
CACHE_TTL=60
MAX_CACHE_SIZE=1000
REDIS_URL=redis://localhost:6379/0

# Network Settings
NETWORK=mainnet-beta
RPC_URL=https://api.mainnet-beta.solana.com
WS_URL=wss://api.mainnet-beta.solana.com

# Hummingbot Settings
HUMMINGBOT_CONNECTOR=orca
HUMMINGBOT_MARKET=SOL-USDC
HUMMINGBOT_STRATEGY=pure_market_making
