"""
Market data collector that fetches data from multiple sources.
"""
import os
import logging
import aiohttp
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MarketDataCollector:
    """Collects market data from various sources."""
    
    def __init__(self):
        self.helius_api_key = os.getenv("HELIUS_API_KEY")
        self.jupiter_api_key = os.getenv("JUPITER_API_KEY")
        self.orca_api_key = os.getenv("ORCA_API_KEY")
        
        # API endpoints
        self.helius_url = "https://api.helius.xyz/v0"
        self.jupiter_url = "https://quote-api.jup.ag/v6"
        self.orca_url = "https://api.orca.so"
        
        # Trading pair
        self.pair = os.getenv("PAIR", "SOL-USDC")
        self.base_token, self.quote_token = self.pair.split("-")
        
        # Cache for recent data
        self.cache = {}
        self.cache_ttl = 30  # seconds
        
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
                "circulating_supply": price_data.get("circulating_supply", 0)
            }
            
            # Cache the data
            self.cache = {
                "data": market_data,
                "timestamp": datetime.utcnow()
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error collecting market data: {str(e)}")
            return self._get_cached_data()
    
    async def _get_price_data(self) -> Dict[str, Any]:
        """Get price data from Jupiter."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get quote
                quote_url = f"{self.jupiter_url}/quote"
                params = {
                    "inputMint": self._get_token_mint(self.base_token),
                    "outputMint": self._get_token_mint(self.quote_token),
                    "amount": "1000000",  # 1 SOL
                    "slippageBps": 50
                }
                
                async with session.get(quote_url, params=params) as response:
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
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.orca_api_key}"}
                url = f"{self.orca_url}/v1/orderbook/{self.pair}"
                
                async with session.get(url, headers=headers) as response:
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
            async with aiohttp.ClientSession() as session:
                url = f"{self.helius_url}/trades"
                params = {
                    "api-key": self.helius_api_key,
                    "pair": self.pair,
                    "limit": 100
                }
                
                async with session.get(url, params=params) as response:
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
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.orca_api_key}"}
                url = f"{self.orca_url}/v1/pools/{self.pair}"
                
                async with session.get(url, headers=headers) as response:
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
        # This is a simplified version - in production, you'd want to maintain a proper token registry
        token_mints = {
            "SOL": "So11111111111111111111111111111111111111112",
            "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        }
        return token_mints.get(token, "") 