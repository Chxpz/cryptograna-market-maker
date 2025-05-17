"""
Monitoring module for the market making bot.
"""
import os
import time
from typing import Dict, Any
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# Metrics
orders_placed = Counter('bot_orders_placed_total', 'Total orders placed')
orders_filled = Counter('bot_orders_filled_total', 'Total orders filled')
orders_cancelled = Counter('bot_orders_cancelled_total', 'Total orders cancelled')
order_errors = Counter('bot_order_errors_total', 'Total order errors')

position_size = Gauge('bot_position_size', 'Current position size')
position_value = Gauge('bot_position_value', 'Current position value in quote currency')
realized_pnl = Gauge('bot_realized_pnl', 'Realized PnL')
unrealized_pnl = Gauge('bot_unrealized_pnl', 'Unrealized PnL')
win_rate = Gauge('bot_win_rate', 'Current win rate')

spread = Gauge('bot_spread', 'Current spread')
volatility = Gauge('bot_volatility', 'Current volatility')
liquidity = Gauge('bot_liquidity', 'Current liquidity')

api_latency = Histogram('bot_api_latency_seconds', 'API request latency', ['endpoint'])
error_count = Counter('bot_errors_total', 'Total errors', ['type'])

class Monitoring:
    """Handles monitoring and metrics collection."""
    
    def __init__(self):
        self.port = int(os.getenv("PROMETHEUS_PORT", "9090"))
        self.update_interval = int(os.getenv("METRICS_UPDATE_INTERVAL", "15"))
        self.is_running = False
        
    def start(self):
        """Start the monitoring server."""
        try:
            start_http_server(self.port)
            self.is_running = True
            return True
        except Exception as e:
            print(f"Failed to start monitoring server: {str(e)}")
            return False
    
    def stop(self):
        """Stop the monitoring server."""
        self.is_running = False
    
    def update_metrics(self, data: Dict[str, Any]):
        """
        Update metrics with current data.
        
        Args:
            data: Dictionary containing current metrics data
        """
        try:
            # Position metrics
            position_size.set(data.get("position_size", 0))
            position_value.set(data.get("position_value", 0))
            realized_pnl.set(data.get("realized_pnl", 0))
            unrealized_pnl.set(data.get("unrealized_pnl", 0))
            win_rate.set(data.get("win_rate", 0))
            
            # Market metrics
            spread.set(data.get("spread", 0))
            volatility.set(data.get("volatility", 0))
            liquidity.set(data.get("liquidity", 0))
            
        except Exception as e:
            error_count.labels(type="metrics_update").inc()
            print(f"Error updating metrics: {str(e)}")
    
    def record_order(self, order_type: str, success: bool):
        """
        Record order metrics.
        
        Args:
            order_type: Type of order (placed, filled, cancelled)
            success: Whether the order was successful
        """
        try:
            if order_type == "placed":
                orders_placed.inc()
            elif order_type == "filled":
                orders_filled.inc()
            elif order_type == "cancelled":
                orders_cancelled.inc()
                
            if not success:
                order_errors.inc()
                
        except Exception as e:
            error_count.labels(type="order_metrics").inc()
            print(f"Error recording order metrics: {str(e)}")
    
    def record_api_latency(self, endpoint: str, duration: float):
        """
        Record API request latency.
        
        Args:
            endpoint: API endpoint
            duration: Request duration in seconds
        """
        try:
            api_latency.labels(endpoint=endpoint).observe(duration)
        except Exception as e:
            error_count.labels(type="latency_metrics").inc()
            print(f"Error recording API latency: {str(e)}")
    
    def record_error(self, error_type: str):
        """
        Record error metrics.
        
        Args:
            error_type: Type of error
        """
        try:
            error_count.labels(type=error_type).inc()
        except Exception as e:
            print(f"Error recording error metrics: {str(e)}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        return {
            "status": "healthy" if self.is_running else "unhealthy",
            "metrics_port": self.port,
            "update_interval": self.update_interval,
            "timestamp": time.time()
        } 