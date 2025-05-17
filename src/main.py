"""
Main trading loop for the market making bot.
"""
import os
import asyncio
import logging
import time
from typing import Dict, Any
from datetime import datetime

from collector.market_data_collector import MarketDataCollector
from decision.trading_strategy import TradingStrategy
from hb_controller import HummingbotController
from monitoring import Monitoring

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketMakingBot:
    """Main bot class that coordinates all components."""
    
    def __init__(self):
        # Initialize components
        self.collector = MarketDataCollector()
        self.strategy = TradingStrategy()
        self.controller = HummingbotController()
        self.monitoring = Monitoring()
        
        # Trading parameters
        self.update_interval = int(os.getenv("UPDATE_INTERVAL", "30"))  # seconds
        self.is_running = False
        
        # Error handling
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.consecutive_errors = 0
        self.max_consecutive_errors = 5
        
        # Circuit breaker
        self.circuit_breaker = False
        self.circuit_breaker_threshold = 0.1  # 10% drawdown
        
    async def start(self):
        """Start the bot."""
        try:
            # Start monitoring
            if not self.monitoring.start():
                raise Exception("Failed to start monitoring")
            
            # Start components
            if not await self.collector.start():
                raise Exception("Failed to start market data collector")
                
            if not await self.controller.start():
                raise Exception("Failed to start Hummingbot controller")
            
            self.is_running = True
            logger.info("Bot started successfully")
            
            # Start main loop
            while self.is_running:
                try:
                    # Check circuit breaker
                    if self.circuit_breaker:
                        logger.warning("Circuit breaker triggered, waiting for reset")
                        await asyncio.sleep(60)  # Wait 1 minute before retrying
                        self.circuit_breaker = False
                        continue
                    
                    # Collect market data
                    start_time = time.time()
                    market_data = await self.collector.collect_market_data()
                    self.monitoring.record_api_latency("market_data", time.time() - start_time)
                    
                    # Check collector health
                    health = await self.collector.health_check()
                    if health["status"] != "healthy":
                        logger.warning(f"Collector health check failed: {health}")
                        self.monitoring.record_error("collector_health")
                        await self._handle_error("collector_health")
                        continue
                    
                    # Calculate trading parameters
                    params = self.strategy.calculate_parameters(market_data)
                    if not params:
                        logger.warning("Failed to calculate trading parameters")
                        self.monitoring.record_error("parameter_calculation")
                        await self._handle_error("parameter_calculation")
                        continue
                    
                    # Update Hummingbot parameters
                    start_time = time.time()
                    success = await self.controller.update_parameters(params)
                    self.monitoring.record_api_latency("update_parameters", time.time() - start_time)
                    
                    if not success:
                        logger.error("Failed to update Hummingbot parameters")
                        self.monitoring.record_error("parameter_update")
                        await self._handle_error("parameter_update")
                        continue
                    
                    # Get performance metrics
                    metrics = self.strategy.get_performance_metrics()
                    self.monitoring.update_metrics(metrics)
                    
                    # Check for circuit breaker conditions
                    if self._check_circuit_breaker(metrics):
                        self.circuit_breaker = True
                        logger.error("Circuit breaker triggered due to drawdown")
                        continue
                    
                    # Reset error counter on success
                    self.consecutive_errors = 0
                    
                    # Wait for next update
                    await asyncio.sleep(self.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in main loop: {str(e)}")
                    self.monitoring.record_error("main_loop")
                    await self._handle_error("main_loop")
                    
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}")
            await self.stop()
            
    async def stop(self):
        """Stop the bot."""
        self.is_running = False
        
        # Stop components
        await self.collector.stop()
        await self.controller.stop()
        self.monitoring.stop()
        
        logger.info("Bot stopped")
    
    async def _handle_error(self, error_type: str):
        """Handle errors and implement recovery procedures."""
        self.consecutive_errors += 1
        
        if self.consecutive_errors >= self.max_consecutive_errors:
            logger.error("Too many consecutive errors, stopping bot")
            await self.stop()
            return
        
        # Implement recovery procedures based on error type
        if error_type == "collector_health":
            # Try to restart collector
            await self.collector.stop()
            await asyncio.sleep(self.retry_delay)
            await self.collector.start()
            
        elif error_type == "parameter_calculation":
            # Use last known good parameters
            logger.info("Using last known good parameters")
            
        elif error_type == "parameter_update":
            # Try to reconnect to Hummingbot
            await self.controller.stop()
            await asyncio.sleep(self.retry_delay)
            await self.controller.start()
            
        elif error_type == "main_loop":
            # General error, wait and retry
            await asyncio.sleep(self.retry_delay)
    
    def _check_circuit_breaker(self, metrics: Dict[str, Any]) -> bool:
        """Check if circuit breaker should be triggered."""
        # Check drawdown
        if "realized_pnl" in metrics and "unrealized_pnl" in metrics:
            total_pnl = metrics["realized_pnl"] + metrics["unrealized_pnl"]
            if total_pnl < -self.circuit_breaker_threshold:
                return True
        
        # Check position size
        if "position_size" in metrics:
            if abs(metrics["position_size"]) > float(os.getenv("MAX_POSITION_SIZE", "100")):
                return True
        
        return False

async def main():
    """Main entry point."""
    bot = MarketMakingBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        await bot.stop()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main()) 