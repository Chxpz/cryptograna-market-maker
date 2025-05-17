#!/bin/bash

# Create necessary directories
mkdir -p hummingbot/conf/connectors
mkdir -p hummingbot/conf/strategies
mkdir -p hummingbot/logs
mkdir -p hummingbot/data
mkdir -p hummingbot/scripts
mkdir -p grafana/dashboards

# Copy configuration files
cp config/config.py src/config/
cp hummingbot/conf/conf_pure_market_making_strategy.yml hummingbot/conf/strategies/
cp grafana/dashboards/market_bot.json grafana/dashboards/

# Set up environment variables
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# API Keys
HELIUS_API_KEY=your_helius_api_key
JUPITER_API_KEY=your_jupiter_api_key
ORCA_API_KEY=your_orca_api_key

# Hummingbot Configuration
HUMMINGBOT_PASSWORD=your_password
HUMMINGBOT_PASSPHRASE=your_passphrase
HUMMINGBOT_API_KEY=your_api_key

# Trading Parameters
TRADING_PAIR=SOL-USDC
MIN_SPREAD=0.001
MAX_SPREAD=0.05
MAX_POSITION_SIZE=100
REBALANCE_THRESHOLD=0.2

# Risk Parameters
MAX_DRAWDOWN=0.1
MAX_LEVERAGE=1.0
MIN_LIQUIDITY=10000

# Analysis Weights
TECHNICAL_WEIGHT=0.4
FUNDAMENTAL_WEIGHT=0.3
SENTIMENT_WEIGHT=0.2
LIQUIDITY_WEIGHT=0.1

# Cache Settings
CACHE_TTL=30

# Logging
LOG_LEVEL=INFO
EOL
    echo "Please edit .env file with your actual values"
fi

# Build and start services
echo "Building and starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check service status
echo "Checking service status..."
docker-compose ps

echo "Initialization complete!"
echo "You can now:"
echo "1. Monitor logs: docker-compose logs -f bot"
echo "2. Access Grafana: http://localhost:3000"
echo "3. Access Prometheus: http://localhost:9090" 