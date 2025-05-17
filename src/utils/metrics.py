"""
Metrics collection for monitoring bot performance.
"""
import os
from typing import Dict, Any
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.port = int(os.getenv("METRICS_PORT", "9090"))
        
        # Initialize metrics
        self.orders_placed = Counter(
            'market_maker_orders_placed_total',
            'Total number of orders placed',
            ['side']
        )
        
        self.orders_filled = Counter(
            'market_maker_orders_filled_total',
            'Total number of orders filled',
            ['side']
        )
        
        self.current_spread = Gauge(
            'market_maker_current_spread',
            'Current spread between bid and ask'
        )
        
        self.profit_loss = Gauge(
            'market_maker_profit_loss',
            'Current profit/loss in USD'
        )
        
        self.order_latency = Histogram(
            'market_maker_order_latency_seconds',
            'Time taken to place orders',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
        )
        
        self.market_data_age = Gauge(
            'market_maker_market_data_age_seconds',
            'Age of market data in seconds'
        )
        
        # Start metrics server
        start_http_server(self.port)
    
    def update(self, market_data: Dict[str, Any], recommendations: Dict[str, Any]):
        """
        Update metrics with latest market data and recommendations.
        
        Args:
            market_data: Current market data
            recommendations: Latest AI recommendations
        """
        # Update spread
        self.current_spread.set(recommendations["spread"])
        
        # Update market data age
        if "timestamp" in market_data:
            data_age = (datetime.utcnow() - datetime.fromisoformat(market_data["timestamp"])).total_seconds()
            self.market_data_age.set(data_age)
    
    def record_order_placed(self, side: str):
        """Record a new order placement."""
        self.orders_placed.labels(side=side).inc()
    
    def record_order_filled(self, side: str):
        """Record an order fill."""
        self.orders_filled.labels(side=side).inc()
    
    def record_profit_loss(self, amount: float):
        """Record profit/loss."""
        self.profit_loss.set(amount)
    
    def record_order_latency(self, seconds: float):
        """Record order placement latency."""
        self.order_latency.observe(seconds) 