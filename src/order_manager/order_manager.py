"""
Order manager for handling market making orders on Solana DEX.
"""
import os
from typing import Dict, Any, List
import asyncio
from datetime import datetime

class OrderManager:
    def __init__(self):
        self.active_orders: Dict[str, Dict[str, Any]] = {}
        self.max_orders = int(os.getenv("MAX_ORDERS", "10"))
        self.min_update_interval = float(os.getenv("MIN_UPDATE_INTERVAL", "1.0"))
        self.last_update = datetime.utcnow()
        
    async def place_orders(self, bid_price: float, ask_price: float, size: float):
        """
        Place new market making orders.
        
        Args:
            bid_price: Price to buy at
            ask_price: Price to sell at
            size: Size of each order in USD
        """
        # Check if we need to update existing orders
        if self._should_update_orders(bid_price, ask_price):
            await self.update_orders({
                "bid_price": bid_price,
                "ask_price": ask_price,
                "size": size
            })
            return
        
        # Cancel existing orders if needed
        if len(self.active_orders) >= self.max_orders:
            await self._cancel_all_orders()
        
        # Place new orders
        bid_order = await self._place_order("bid", bid_price, size)
        ask_order = await self._place_order("ask", ask_price, size)
        
        # Store order information
        self.active_orders[bid_order["id"]] = bid_order
        self.active_orders[ask_order["id"]] = ask_order
        
        self.last_update = datetime.utcnow()
    
    async def update_orders(self, recommendations: Dict[str, Any]):
        """
        Update existing orders based on new recommendations.
        
        Args:
            recommendations: Dictionary containing new price recommendations
        """
        current_time = datetime.utcnow()
        if (current_time - self.last_update).total_seconds() < self.min_update_interval:
            return
        
        # Update each active order
        for order_id, order in list(self.active_orders.items()):
            new_price = (
                recommendations["bid_price"] if order["side"] == "bid"
                else recommendations["ask_price"]
            )
            
            # Only update if price difference is significant
            if abs(new_price - order["price"]) / order["price"] > 0.001:
                await self._update_order(order_id, new_price)
        
        self.last_update = current_time
    
    async def _place_order(self, side: str, price: float, size: float) -> Dict[str, Any]:
        """Place a single order on the DEX."""
        # This is a placeholder that should be implemented with actual DEX SDK
        order = {
            "id": f"{side}_{datetime.utcnow().timestamp()}",
            "side": side,
            "price": price,
            "size": size,
            "status": "open",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Simulate order placement
        print(f"Placing {side} order: {price} @ {size}")
        
        return order
    
    async def _update_order(self, order_id: str, new_price: float):
        """Update an existing order with new price."""
        if order_id not in self.active_orders:
            return
        
        order = self.active_orders[order_id]
        
        # Cancel existing order
        await self._cancel_order(order_id)
        
        # Place new order
        new_order = await self._place_order(
            order["side"],
            new_price,
            order["size"]
        )
        
        # Update order tracking
        del self.active_orders[order_id]
        self.active_orders[new_order["id"]] = new_order
    
    async def _cancel_order(self, order_id: str):
        """Cancel a single order."""
        if order_id in self.active_orders:
            # Simulate order cancellation
            print(f"Cancelling order: {order_id}")
            del self.active_orders[order_id]
    
    async def _cancel_all_orders(self):
        """Cancel all active orders."""
        for order_id in list(self.active_orders.keys()):
            await self._cancel_order(order_id)
    
    def _should_update_orders(self, bid_price: float, ask_price: float) -> bool:
        """Determine if existing orders should be updated."""
        if not self.active_orders:
            return False
        
        # Check if any active orders are too far from new prices
        for order in self.active_orders.values():
            current_price = order["price"]
            target_price = bid_price if order["side"] == "bid" else ask_price
            
            if abs(current_price - target_price) / current_price > 0.001:
                return True
        
        return False
    
    def get_active_orders(self) -> List[Dict[str, Any]]:
        """Get list of all active orders."""
        return list(self.active_orders.values()) 