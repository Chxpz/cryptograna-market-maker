# Solana Market Making Bot

A high-performance market making bot for Solana DEXes, built with Python and Hummingbot.

## Features

### Core Components
- **Market Data Collector**: Real-time data collection from multiple sources with validation and rate limiting
- **Trading Strategy**: Pure market making with dynamic parameter adjustment
- **Hummingbot Controller**: Order execution and parameter management
- **Monitoring System**: Prometheus metrics and Grafana dashboards

### Key Features
- Real-time market data collection from Helius, Jupiter, and Orca
- Dynamic spread and order size calculation
- Position tracking and risk management
- Circuit breakers for drawdown protection
- Comprehensive monitoring and metrics
- Automated error recovery
- Rate limiting and caching

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Hummingbot instance
- API keys for:
  - Helius
  - Jupiter
  - Orca

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/solana-market-making-bot.git
cd solana-market-making-bot
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

## Monitoring

The bot provides comprehensive monitoring through:

### Metrics
- Order metrics (placed, filled, cancelled)
- Position metrics (size, value, PnL)
- Market metrics (spread, volatility, liquidity)
- API latency
- Error counts

### Health Checks
- Component health status
- API connectivity
- Data validation
- Error tracking

### Alerts
- Circuit breaker triggers
- Error thresholds
- Performance degradation
- API issues

## Error Recovery

The bot implements automatic error recovery for:
- API connection issues
- Data validation failures
- Parameter calculation errors
- Order execution failures

## Development

### Project Structure
```
.
├── src/
│   ├── collector/         # Market data collection
│   ├── decision/          # Trading strategy
│   ├── monitoring/        # Metrics and monitoring
│   └── main.py           # Main trading loop
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── docker/              # Docker configuration
```

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hummingbot for the trading infrastructure
- Helius, Jupiter, and Orca for market data
- Prometheus and Grafana for monitoring
