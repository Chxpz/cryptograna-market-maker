# Solana Market Making Bot

A sophisticated market making bot for Solana DEXs that uses multiple analysis methods to make trading decisions.

## Features

- Real-time market data collection from multiple sources
- Multi-factor analysis:
  - Technical analysis (SMA, EMA, RSI, MACD, Bollinger Bands)
  - Fundamental analysis (market cap, volume, liquidity)
  - Sentiment analysis (social, news, market sentiment)
  - Liquidity analysis (order book depth, spread, slippage)
  - Risk analysis (volatility, drawdown, concentration)
- Automated trading strategies:
  - Market making
  - Arbitrage
  - Liquidity provision
- Real-time monitoring and metrics
- Risk management and position sizing
- Docker-based deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- API keys for:
  - Helius
  - Jupiter
  - Orca

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/solana-market-bot.git
cd solana-market-bot
```

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your API keys and configuration:
```bash
# API Keys
HELIUS_API_KEY=your_helius_api_key
JUPITER_API_KEY=your_jupiter_api_key
ORCA_API_KEY=your_orca_api_key

# Other settings...
```

4. Build and start the services:
```bash
docker-compose up -d
```

5. Monitor the logs:
```bash
docker-compose logs -f bot
```

## Configuration

The bot can be configured through environment variables in the `.env` file:

### Trading Parameters
- `TRADING_PAIR`: Trading pair (default: SOL-USDC)
- `MIN_SPREAD`: Minimum spread (default: 0.001)
- `MAX_SPREAD`: Maximum spread (default: 0.05)
- `MAX_POSITION_SIZE`: Maximum position size (default: 100)
- `REBALANCE_THRESHOLD`: Rebalancing threshold (default: 0.2)

### Risk Parameters
- `MAX_DRAWDOWN`: Maximum drawdown (default: 0.1)
- `MAX_LEVERAGE`: Maximum leverage (default: 1.0)
- `MIN_LIQUIDITY`: Minimum liquidity (default: 10000)

### Analysis Weights
- `TECHNICAL_WEIGHT`: Technical analysis weight (default: 0.4)
- `FUNDAMENTAL_WEIGHT`: Fundamental analysis weight (default: 0.3)
- `SENTIMENT_WEIGHT`: Sentiment analysis weight (default: 0.2)
- `LIQUIDITY_WEIGHT`: Liquidity analysis weight (default: 0.1)

## Monitoring

The bot includes several monitoring tools:

- Prometheus: Metrics collection
- Grafana: Metrics visualization (http://localhost:3000)
- Redis: Caching and real-time data
- PostgreSQL: Historical data storage
- Qdrant: Vector database for similarity search

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Run linting:
```bash
flake8
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

### Completed
- Project structure
- Environment configuration
- Market analysis system
  - Technical analysis
  - Fundamental analysis
  - Sentiment analysis
  - Liquidity analysis
  - Risk analysis

### In Progress
- Data collection system
- Trading strategies
- Monitoring system

### Upcoming
- Testing framework
- Documentation
- Performance optimization
- Security enhancements
- Deployment automation
- Additional features

### Future Considerations
- Advanced trading strategies
- Machine learning integration
- Community features
- Enterprise features
