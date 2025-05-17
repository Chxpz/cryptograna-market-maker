#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Check required environment variables
required_vars=(
    "HELIUS_API_KEY"
    "JUPITER_API_KEY"
    "ORCA_API_KEY"
    "HUMMINGBOT_URL"
    "HUMMINGBOT_API_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set in .env file"
        exit 1
    fi
done

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the bot with proper logging
echo "Starting market making bot..."
python src/main.py 2>&1 | tee -a "logs/bot_$(date +%Y%m%d_%H%M%S).log"

# Check exit status
if [ $? -eq 0 ]; then
    echo "Bot stopped successfully"
else
    echo "Bot stopped with errors. Check logs for details."
    exit 1
fi 