"""
Configuration settings for the market making bot.
"""
import os
from typing import Dict, Any

# API Keys
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
JUPITER_API_KEY = os.getenv("JUPITER_API_KEY")
ORCA_API_KEY = os.getenv("ORCA_API_KEY")

# Database URLs
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/market_bot")

# Monitoring
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

# Trading Parameters
TRADING_PAIR = os.getenv("TRADING_PAIR", "SOL-USDC")
MIN_SPREAD = float(os.getenv("MIN_SPREAD", "0.001"))
MAX_SPREAD = float(os.getenv("MAX_SPREAD", "0.05"))
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "100"))
REBALANCE_THRESHOLD = float(os.getenv("REBALANCE_THRESHOLD", "0.2"))

# Risk Parameters
MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", "0.1"))
MAX_LEVERAGE = float(os.getenv("MAX_LEVERAGE", "1.0"))
MIN_LIQUIDITY = float(os.getenv("MIN_LIQUIDITY", "10000"))

# Analysis Parameters
TECHNICAL_WEIGHT = float(os.getenv("TECHNICAL_WEIGHT", "0.4"))
FUNDAMENTAL_WEIGHT = float(os.getenv("FUNDAMENTAL_WEIGHT", "0.3"))
SENTIMENT_WEIGHT = float(os.getenv("SENTIMENT_WEIGHT", "0.2"))
LIQUIDITY_WEIGHT = float(os.getenv("LIQUIDITY_WEIGHT", "0.1"))

# Cache Settings
CACHE_TTL = int(os.getenv("CACHE_TTL", "30"))  # seconds

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_config() -> Dict[str, Any]:
    """Get all configuration settings as a dictionary."""
    return {
        "api_keys": {
            "helius": HELIUS_API_KEY,
            "jupiter": JUPITER_API_KEY,
            "orca": ORCA_API_KEY
        },
        "database": {
            "redis": REDIS_URL,
            "qdrant": QDRANT_URL,
            "postgres": POSTGRES_URL
        },
        "monitoring": {
            "prometheus": PROMETHEUS_URL
        },
        "trading": {
            "pair": TRADING_PAIR,
            "min_spread": MIN_SPREAD,
            "max_spread": MAX_SPREAD,
            "max_position_size": MAX_POSITION_SIZE,
            "rebalance_threshold": REBALANCE_THRESHOLD
        },
        "risk": {
            "max_drawdown": MAX_DRAWDOWN,
            "max_leverage": MAX_LEVERAGE,
            "min_liquidity": MIN_LIQUIDITY
        },
        "analysis": {
            "technical_weight": TECHNICAL_WEIGHT,
            "fundamental_weight": FUNDAMENTAL_WEIGHT,
            "sentiment_weight": SENTIMENT_WEIGHT,
            "liquidity_weight": LIQUIDITY_WEIGHT
        },
        "cache": {
            "ttl": CACHE_TTL
        },
        "logging": {
            "level": LOG_LEVEL,
            "format": LOG_FORMAT
        }
    } 