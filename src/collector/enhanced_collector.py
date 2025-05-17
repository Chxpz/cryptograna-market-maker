"""
Enhanced data collector that combines data from multiple sources.
"""
import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
import aiohttp
from dotenv import load_dotenv

# Configuration
load_dotenv()
logger = logging.getLogger(__name__)

class EnhancedDataCollector:
    def __init__(self):
        # Initialize storage clients
        self.qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        self.collection_name = "enhanced_market_data"
        self.vector_size = 256  # Increased vector size for more features
        
        # Initialize collection
        self._init_collection()
        
        # API configurations
        self.helius_api_key = os.getenv("HELIUS_API_KEY")
        self.helius_url = f"https://api.helius.xyz/v0/token-metadata?api-key={self.helius_api_key}"
        self.jupiter_url = "https://quote-api.jup.ag/v6"
        self.orca_url = "https://api.orca.so"
        
        # Data retention configuration
        self.retention_periods = {
            "1m": timedelta(days=7),
            "5m": timedelta(days=30),
            "1h": timedelta(days=90),
            "1d": timedelta(days=365)
        }
        
    def _init_collection(self):
        """Initialize Qdrant collection with proper configuration."""
        collections = self.qdrant.get_collections().collections
        exists = any(col.name == self.collection_name for col in collections)
        
        if not exists:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Collection {self.collection_name} created in Qdrant")
    
    async def collect_data(self) -> Dict[str, Any]:
        """
        Collect data from all sources concurrently.
        """
        try:
            # Collect from all sources
            price_data, orderbook_data, liquidity_data, volume_data = await asyncio.gather(
                self._collect_price_data(),
                self._collect_orderbook_data(),
                self._collect_liquidity_data(),
                self._collect_volume_data()
            )
            
            # Combine and process data
            market_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "price": price_data,
                "orderbook": orderbook_data,
                "liquidity": liquidity_data,
                "volume": volume_data,
                "metrics": self._calculate_metrics(price_data, orderbook_data, liquidity_data, volume_data)
            }
            
            # Store data
            await self._store_data(market_data)
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error collecting data: {e}")
            return {}
    
    async def _collect_price_data(self) -> Dict[str, Any]:
        """Collect price data from multiple sources."""
        async with aiohttp.ClientSession() as session:
            # Collect from Helius
            helius_data = await self._get_helius_data(session)
            
            # Collect from Jupiter
            jupiter_data = await self._get_jupiter_data(session)
            
            # Combine and validate data
            return self._combine_price_data(helius_data, jupiter_data)
    
    async def _collect_orderbook_data(self) -> Dict[str, Any]:
        """Collect orderbook data from Orca."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.orca_url}/orderbook"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_orderbook_data(data)
                else:
                    raise Exception(f"Failed to fetch orderbook data: {response.status}")
    
    async def _collect_liquidity_data(self) -> Dict[str, Any]:
        """Collect liquidity data from multiple sources."""
        async with aiohttp.ClientSession() as session:
            # Collect from Orca pools
            orca_data = await self._get_orca_liquidity(session)
            
            # Collect from Jupiter routes
            jupiter_data = await self._get_jupiter_liquidity(session)
            
            return self._combine_liquidity_data(orca_data, jupiter_data)
    
    async def _collect_volume_data(self) -> Dict[str, Any]:
        """Collect volume data from multiple sources."""
        async with aiohttp.ClientSession() as session:
            # Collect from Helius
            helius_data = await self._get_helius_volume(session)
            
            # Collect from Orca
            orca_data = await self._get_orca_volume(session)
            
            return self._combine_volume_data(helius_data, orca_data)
    
    def _calculate_metrics(self, price_data: Dict, orderbook_data: Dict,
                         liquidity_data: Dict, volume_data: Dict) -> Dict[str, float]:
        """Calculate derived metrics from collected data."""
        return {
            "volatility": self._calculate_volatility(price_data),
            "spread": self._calculate_spread(orderbook_data),
            "liquidity_score": self._calculate_liquidity_score(liquidity_data),
            "volume_score": self._calculate_volume_score(volume_data),
            "market_impact": self._calculate_market_impact(orderbook_data, volume_data)
        }
    
    async def _store_data(self, data: Dict[str, Any]):
        """Store data in Qdrant with proper indexing."""
        try:
            # Create vector representation
            vector = self._create_market_vector(data)
            
            # Store in Qdrant
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=int(datetime.utcnow().timestamp() * 1000),
                        vector=vector.tolist(),
                        payload=data
                    )
                ]
            )
            
            # Clean up old data
            await self._cleanup_old_data()
            
        except Exception as e:
            logger.error(f"Error storing data: {e}")
    
    def _create_market_vector(self, data: Dict[str, Any]) -> np.ndarray:
        """Create vector representation of market data."""
        features = [
            data["price"].get("current", 0),
            data["price"].get("change_24h", 0),
            data["orderbook"].get("spread", 0),
            data["liquidity"].get("total", 0),
            data["volume"].get("24h", 0),
            data["metrics"].get("volatility", 0),
            data["metrics"].get("liquidity_score", 0),
            data["metrics"].get("volume_score", 0),
            data["metrics"].get("market_impact", 0)
        ]
        
        # Pad to vector size
        features = features + [0] * (self.vector_size - len(features))
        return np.array(features, dtype=np.float32)
    
    async def _cleanup_old_data(self):
        """Clean up data older than retention periods."""
        try:
            for interval, retention in self.retention_periods.items():
                cutoff_time = datetime.utcnow() - retention
                
                # Delete old data
                self.qdrant.delete(
                    collection_name=self.collection_name,
                    points_selector=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="timestamp",
                                range=models.Range(
                                    lt=cutoff_time.isoformat()
                                )
                            )
                        ]
                    )
                )
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    async def get_similar_market_conditions(self, current_data: Dict[str, Any],
                                          limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar market conditions in historical data."""
        try:
            # Create vector for current data
            vector = self._create_market_vector(current_data)
            
            # Search for similar points
            search_result = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=vector.tolist(),
                limit=limit
            )
            
            return [point.payload for point in search_result]
            
        except Exception as e:
            logger.error(f"Error finding similar conditions: {e}")
            return []
    
    async def get_historical_data(self, start_time: Optional[datetime] = None,
                                end_time: Optional[datetime] = None,
                                interval: str = "1h",
                                limit: int = 1000) -> List[Dict[str, Any]]:
        """Get historical data for analysis."""
        try:
            # Build time filter
            filter_condition = models.Filter(
                must=[
                    models.FieldCondition(
                        key="timestamp",
                        range=models.Range(
                            gt=start_time.isoformat() if start_time else None,
                            lt=end_time.isoformat() if end_time else None
                        )
                    )
                ]
            )
            
            # Get data
            search_result = self.qdrant.scroll(
                collection_name=self.collection_name,
                filter=filter_condition,
                limit=limit
            )
            
            return [point.payload for point in search_result[0]]
            
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            return [] 