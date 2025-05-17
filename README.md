# Solana Market Making Bot

A sophisticated market making bot for Solana DEXes, built with Python and Hummingbot.

## Features

- **Multi-Strategy Support**: Implements market making, arbitrage, and liquidity provision strategies
- **Advanced Data Collection**: Collects and analyzes market data from multiple sources
- **Intelligent Decision Making**: Uses AI to analyze market conditions and make trading decisions
- **Risk Management**: Implements comprehensive risk management and position sizing
- **Performance Monitoring**: Tracks and analyzes bot performance with detailed metrics
- **Hummingbot Integration**: Seamlessly integrates with Hummingbot for order execution

## Architecture

### Core Components

1. **Data Collection**
   - Enhanced data collector for multiple sources
   - Real-time market data processing
   - Efficient data storage and retrieval
   - Historical data analysis

2. **Market Analysis**
   - Technical analysis
   - Fundamental analysis
   - Sentiment analysis
   - Liquidity analysis
   - Risk analysis

3. **Decision Engine**
   - Strategy evaluation and selection
   - Action generation
   - Risk management
   - Performance tracking

4. **Trading Strategies**
   - Market Making
   - Arbitrage
   - Liquidity Provision

5. **Performance Monitoring**
   - Real-time metrics tracking
   - Performance analysis
   - Insight generation
   - Risk monitoring

### Technical Implementation

#### Data Collection
- Uses Qdrant for vector storage
- Redis for caching
- Prometheus for metrics
- PostgreSQL for general data storage
- Retention periods:
  - Time series data: 30 days
  - Vector storage: 90 days
  - Cache: 1 hour

#### Market Analysis
- Combines multiple analysis methods
- Weighted scoring system
- Confidence calculation
- Market regime detection
- Trend analysis
- Volatility measurement
- Liquidity assessment
- Risk evaluation

#### Decision Engine
- Strategy weights:
  - Market Making: 40%
  - Arbitrage: 30%
  - Liquidity Provision: 30%
- Risk parameters:
  - Maximum position size
  - Maximum drawdown
  - Maximum leverage
  - Minimum liquidity
- Performance tracking:
  - Total PnL
  - Win rate
  - Sharpe ratio
  - Maximum drawdown

#### Trading Strategies

##### Market Making
- Minimum spread: 0.1%
- Maximum position: 100 units
- Rebalance threshold: 20%
- Dynamic spread adjustment based on volatility
- Position size scaling based on current position

##### Arbitrage
- Minimum profit threshold: 0.2%
- Maximum slippage: 0.1%
- Maximum position: 50 units
- Position size based on liquidity and profit potential
- Slippage protection

##### Liquidity Provision
- Minimum liquidity threshold: 10,000 units
- Maximum position: 200 units
- Rebalance threshold: 30%
- Dynamic position sizing based on liquidity gap
- Volatility-based adjustments

#### Performance Monitoring

##### Metrics
- Profitability:
  - Total PnL
  - Win rate
  - Sharpe ratio
  - Maximum drawdown
- Risk:
  - Position size
  - Leverage
  - Volatility
- Execution:
  - Order count
  - Execution time
  - Slippage
- Market Impact:
  - Spread
  - Liquidity
  - Volume

##### Analysis
- 7-day analysis window
- Minimum 10 trades for analysis
- Risk-free rate: 2%
- Performance insights
- Risk warnings
- Strategy suggestions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the bot:
```bash
python src/main.py
```

## Configuration

### Environment Variables
- `HELIUS_API_KEY`: Helius API key for market data
- `JUPITER_API_KEY`: Jupiter API key for price data
- `ORCA_API_KEY`: Orca API key for liquidity data
- `MAX_POSITION_SIZE`: Maximum position size
- `MAX_DRAWDOWN`: Maximum drawdown limit
- `MAX_LEVERAGE`: Maximum leverage limit
- `MIN_LIQUIDITY`: Minimum liquidity requirement

### Strategy Parameters
- Market Making:
  - `MIN_SPREAD`: Minimum spread (default: 0.001)
  - `MAX_POSITION`: Maximum position size (default: 100)
  - `REBALANCE_THRESHOLD`: Position rebalance threshold (default: 0.2)
- Arbitrage:
  - `MIN_PROFIT_THRESHOLD`: Minimum profit threshold (default: 0.002)
  - `MAX_SLIPPAGE`: Maximum allowed slippage (default: 0.001)
  - `MAX_POSITION`: Maximum position size (default: 50)
- Liquidity Provision:
  - `MIN_LIQUIDITY_THRESHOLD`: Minimum liquidity threshold (default: 10000)
  - `MAX_POSITION`: Maximum position size (default: 200)
  - `REBALANCE_THRESHOLD`: Position rebalance threshold (default: 0.3)

## Monitoring

### Prometheus Metrics
- `bot_total_pnl`: Total PnL in USD
- `bot_win_rate`: Win rate percentage
- `bot_sharpe_ratio`: Sharpe ratio
- `bot_max_drawdown`: Maximum drawdown percentage
- `bot_position_size`: Current position size
- `bot_leverage`: Current leverage
- `bot_volatility`: Current market volatility
- `bot_order_count`: Total number of orders
- `bot_execution_time`: Order execution time in seconds
- `bot_slippage`: Order slippage percentage
- `bot_spread`: Current market spread
- `bot_liquidity`: Current market liquidity
- `bot_volume`: Current market volume

### Performance Analysis
- Real-time performance tracking
- 7-day analysis window
- Minimum 10 trades required
- Risk-adjusted return calculation
- Position and execution analysis
- Market impact assessment
- Automated insights and suggestions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
