"""
Hummingbot Controller for managing order execution and strategy parameters.
"""
import os
import json
import logging
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class HummingbotController:
    """Manages interaction with Hummingbot for order execution."""
    
    def __init__(self):
        self.url = os.getenv("HUMMINGBOT_URL", "http://localhost:9000")
        self.api_key = os.getenv("HUMMINGBOT_API_KEY")
        self.connector = os.getenv("HUMMINGBOT_CONNECTOR", "orca")
        self.market = os.getenv("HUMMINGBOT_MARKET", "SOL-USDC")
        self.strategy = os.getenv("HUMMINGBOT_STRATEGY", "pure_market_making")
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.is_running = False
        self.last_error = None
        self.error_count = 0
        self.max_retries = 3
        
        # Order tracking
        self.active_orders = {}
        self.position = 0.0
        self.last_update = None
        
    async def start(self):
        """Start the controller and initialize connection."""
        try:
            self.session = aiohttp.ClientSession()
            self.is_running = True
            
            # Start strategy
            await self._start_strategy()
            
            # Start order tracking
            asyncio.create_task(self._track_orders())
            
            logger.info("Hummingbot controller started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Hummingbot controller: {str(e)}")
            self.last_error = str(e)
            return False
    
    async def stop(self):
        """Stop the controller and clean up resources."""
        self.is_running = False
        
        try:
            # Cancel all orders
            await self._cancel_all_orders()
            
            # Stop strategy
            await self._stop_strategy()
            
            # Close session
            if self.session:
                await self.session.close()
                
            logger.info("Hummingbot controller stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping Hummingbot controller: {str(e)}")
            return False
    
    async def update_parameters(self, params: Dict[str, Any]) -> bool:
        """
        Update strategy parameters.
        
        Args:
            params: Dictionary containing strategy parameters
            
        Returns:
            bool: True if update was successful
        """
        try:
            # Validate parameters
            if not self._validate_parameters(params):
                logger.error("Invalid parameters")
                return False
            
            # Update strategy parameters
            endpoint = f"{self.url}/api/v1/strategy/update"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            data = {
                "strategy": self.strategy,
                "parameters": {
                    "bid_spread": params.get("bid_spread", 0.001),
                    "ask_spread": params.get("ask_spread", 0.001),
                    "order_amount": params.get("order_amount", 1.0),
                    "order_refresh_time": params.get("order_refresh_time", 60),
                    "inventory_skew_enabled": params.get("inventory_skew_enabled", True),
                    "target_base_pct": params.get("target_base_pct", 0.5)
                }
            }
            
            async with self.session.post(endpoint, json=data, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to update parameters: {await response.text()}")
                    return False
                    
                self.last_update = datetime.utcnow()
                logger.info("Strategy parameters updated successfully")
                return True
            if not self.session:
                raise Exception("Controller not started")
                
            # Extract parameters
            params = recommendations.get("parameters", {})
            spread = params.get("spread", 0.001)
            position_size = params.get("position_size", 0.0)
            
            # Prepare configuration
            config = {
                "strategy": "pure_market_making",
                "exchange": "orca",
                "trading_pair": os.getenv("TRADING_PAIR", "SOL-USDC"),
                "bid_spread": spread,
                "ask_spread": spread,
                "order_amount": position_size,
                "order_refresh_time": 30,
                "max_order_age": 1800,
                "order_refresh_tolerance_pct": 0.1,
                "cancel_order_wait_time": 60,
                "enable_order_filled_stop_cancellation": True,
                "filled_order_delay": 60,
                "inventory_skew_enabled": True,
                "inventory_target_base_pct": 0.5,
                "inventory_range_multiplier": 0.1,
                "volatility_buffer_size": 30,
                "volatility_interval": 60,
                "volatility_to_spread_multiplier": 1.0,
                "max_spread": float(os.getenv("MAX_SPREAD", "0.05")),
                "min_spread": float(os.getenv("MIN_SPREAD", "0.001")),
                "status_report_interval": 900
            }
            
            # Update configuration
            async with self.session.post(
                f"{self.hb_url}/config",
                json=config
            ) as response:
                if response.status == 200:
                    logger.info("Hummingbot parameters updated successfully")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Failed to update parameters: {error}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating parameters: {str(e)}")
            return False
            
    async def get_status(self) -> Dict[str, Any]:
        """Get current Hummingbot status."""
        try:
            if not self.session:
                raise Exception("Controller not started")
                
            async with self.session.get(f"{self.hb_url}/status") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error = await response.text()
                    logger.error(f"Failed to get status: {error}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting status: {str(e)}")
            return {}
            
    async def start_strategy(self) -> bool:
        """Start the trading strategy."""
        try:
            if not self.session:
                raise Exception("Controller not started")
                
            async with self.session.post(f"{self.hb_url}/start") as response:
                if response.status == 200:
                    logger.info("Strategy started successfully")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Failed to start strategy: {error}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error starting strategy: {str(e)}")
            return False
            
    async def stop_strategy(self) -> bool:
        """Stop the trading strategy."""
        try:
            if not self.session:
                raise Exception("Controller not started")
                
            async with self.session.post(f"{self.hb_url}/stop") as response:
                if response.status == 200:
                    logger.info("Strategy stopped successfully")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Failed to stop strategy: {error}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error stopping strategy: {str(e)}")
            return False 