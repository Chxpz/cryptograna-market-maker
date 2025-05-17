"""
Market data collector that fetches data from multiple sources.
"""
import os
import logging
import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from aiohttp import ClientTimeout
from ratelimit import limits, sleep_and_retry

logger = logging.getLogger(__name__)

@dataclass
class DataValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.last_reset = datetime.utcnow()
        self.calls_made = 0
        
    async def acquire(self):
        """Acquire a rate limit token."""
        now = datetime.utcnow()
        if (now - self.last_reset).total_seconds() >= self.period:
            self.calls_made = 0
            self.last_reset = now
            
        if self.calls_made >= self.calls:
            wait_time = self.period - (now - self.last_reset).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                self.calls_made = 0
                self.last_reset = datetime.utcnow()
                
        self.calls_made += 1

class MarketDataCollector:
    """Collects market data from various sources."""
    
    def __init__(self):
        # API keys
        self.helius_api_key = os.getenv("HELIUS_API_KEY")
        self.jupiter_api_key = os.getenv("JUPITER_API_KEY")
        self.orca_api_key = os.getenv("ORCA_API_KEY")
        
        if not all([self.helius_api_key, self.jupiter_api_key, self.orca_api_key]):
            raise ValueError("Missing required API keys")
        
        # API endpoints
        self.helius_url = "https://api.helius.xyz/v0"
        self.jupiter_url = "https://quote-api.jup.ag/v6"
        self.orca_url = "https://api.orca.so"
        
        # Trading pair
        self.pair = os.getenv("TRADING_PAIR", "SOL-USDC")
        self.base_token, self.quote_token = self.pair.split("-")
        
        # Cache configuration
        self.cache = {}
        self.cache_ttl = int(os.getenv("CACHE_TTL", "30"))
        
        # Rate limiters
        self.helius_limiter = RateLimiter(calls=10, period=1)  # 10 calls per second
        self.jupiter_limiter = RateLimiter(calls=5, period=1)   # 5 calls per second
        self.orca_limiter = RateLimiter(calls=20, period=1)     # 20 calls per second
        
        # Health check
        self.last_successful_collection = None
        self.consecutive_failures = 0
        self.max_failures = int(os.getenv("MAX_CONSECUTIVE_FAILURES", "3"))
        
        # HTTP client configuration
        self.timeout = ClientTimeout(total=10)  # 10 seconds timeout
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def start(self):
        """Start the collector and initialize HTTP session."""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        logger.info("Market data collector started")
        
    async def stop(self):
        """Stop the collector and cleanup."""
        if self.session:
            await self.session.close()
        logger.info("Market data collector stopped")
        
    async def collect_market_data(self) -> Dict[str, Any]:
        """
        Collect market data from all sources.
        
        Returns:
            Dictionary containing combined market data
        """
        try:
            # Collect data concurrently
            price_data, order_book, trades = await asyncio.gather(
                self._get_price_data(),
                self._get_order_book(),
                self._get_recent_trades()
            )
            
            # Validate collected data
            validation = self._validate_data(price_data, order_book, trades)
            if not validation.is_valid:
                logger.warning(f"Data validation warnings: {validation.warnings}")
                if validation.errors:
                    raise ValueError(f"Data validation errors: {validation.errors}")
            
            # Combine data
            market_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "pair": self.pair,
                "price": price_data["price"],
                "volume_24h": price_data["volume_24h"],
                "order_book": order_book,
                "trades": trades,
                "liquidity_pools": await self._get_liquidity_pools(),
                "market_cap": price_data.get("market_cap", 0),
                "total_supply": price_data.get("total_supply", 0),
                "circulating_supply": price_data.get("circulating_supply", 0),
                "validation": {
                    "warnings": validation.warnings,
                    "errors": validation.errors
                }
            }
            
            # Cache the data
            self.cache = {
                "data": market_data,
                "timestamp": datetime.utcnow()
            }
            
            # Update health check
            self.last_successful_collection = datetime.utcnow()
            self.consecutive_failures = 0
            
            return market_data
            
        except Exception as e:
            self.consecutive_failures += 1
            logger.error(f"Error collecting market data: {str(e)}")
            
            if self.consecutive_failures >= self.max_failures:
                logger.error("Maximum consecutive failures reached. Using cached data.")
                return self._get_cached_data()
            
            raise
    
    def _validate_data(self, price_data: Dict, order_book: Dict, trades: List) -> DataValidationResult:
        """Validate collected data."""
        errors = []
        warnings = []
        
        # Validate price data
        if not price_data.get("price", 0) > 0:
            errors.append("Invalid price data")
        if not price_data.get("volume_24h", 0) >= 0:
            warnings.append("Invalid volume data")
            
        # Validate order book
        if not order_book.get("bids") or not order_book.get("asks"):
            warnings.append("Empty order book")
        else:
            if not all(bid["price"] > 0 for bid in order_book["bids"]):
                errors.append("Invalid bid prices")
            if not all(ask["price"] > 0 for ask in order_book["asks"]):
                errors.append("Invalid ask prices")
                
        # Validate trades
        if not trades:
            warnings.append("No recent trades")
        else:
            if not all(trade.get("price", 0) > 0 for trade in trades):
                errors.append("Invalid trade prices")
                
        return DataValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def _get_price_data(self) -> Dict[str, Any]:
        """Get price data from Jupiter."""
        try:
            await self.jupiter_limiter.acquire()
            
            async with self.session.get(
                f"{self.jupiter_url}/quote",
                params={
                    "inputMint": self._get_token_mint(self.base_token),
                    "outputMint": self._get_token_mint(self.quote_token),
                    "amount": "1000000",  # 1 SOL
                    "slippageBps": 50
                }
            ) as response:
                if response.status == 200:
                    quote_data = await response.json()
                    return {
                        "price": float(quote_data["outAmount"]) / 1000000,
                        "volume_24h": float(quote_data.get("volume24h", 0))
                    }
                else:
                    raise Exception(f"Jupiter API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error getting price data: {str(e)}")
            return {"price": 0, "volume_24h": 0}
    
    async def _get_order_book(self) -> Dict[str, List[Dict[str, float]]]:
        """Get order book data from Orca."""
        try:
            await self.orca_limiter.acquire()
            
            async with self.session.get(
                f"{self.orca_url}/v1/orderbook/{self.pair}",
                headers={"Authorization": f"Bearer {self.orca_api_key}"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "bids": data["bids"],
                        "asks": data["asks"]
                    }
                else:
                    raise Exception(f"Orca API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error getting order book: {str(e)}")
            return {"bids": [], "asks": []}
    
    async def _get_recent_trades(self) -> List[Dict[str, Any]]:
        """Get recent trades from Helius."""
        try:
            await self.helius_limiter.acquire()
            
            async with self.session.get(
                f"{self.helius_url}/trades",
                params={
                    "api-key": self.helius_api_key,
                    "pair": self.pair,
                    "limit": 100
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Helius API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error getting recent trades: {str(e)}")
            return []
    
    async def _get_liquidity_pools(self) -> List[Dict[str, Any]]:
        """Get liquidity pool data from Orca."""
        try:
            await self.orca_limiter.acquire()
            
            async with self.session.get(
                f"{self.orca_url}/v1/pools/{self.pair}",
                headers={"Authorization": f"Bearer {self.orca_api_key}"}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Orca API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error getting liquidity pools: {str(e)}")
            return []
    
    def _get_cached_data(self) -> Dict[str, Any]:
        """Get cached data if available and not expired."""
        if "data" in self.cache:
            cache_age = datetime.utcnow() - self.cache["timestamp"]
            if cache_age.total_seconds() < self.cache_ttl:
                return self.cache["data"]
        return {}
    
    def _get_token_mint(self, token: str) -> str:
        """Get token mint address."""
        token_mints = {
            "SOL": "So11111111111111111111111111111111111111112",
            "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        }
        return token_mints.get(token, "")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the data collector."""
        return {
            "status": "healthy" if self.consecutive_failures < self.max_failures else "unhealthy",
            "last_successful_collection": self.last_successful_collection.isoformat() if self.last_successful_collection else None,
            "consecutive_failures": self.consecutive_failures,
            "cache_status": {
                "has_data": "data" in self.cache,
                "age_seconds": (datetime.utcnow() - self.cache["timestamp"]).total_seconds() if "data" in self.cache else None
            }
        } 