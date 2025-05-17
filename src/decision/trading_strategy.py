"""
Trading strategy implementation for market making.
"""
import os
import logging
import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Position:
    base_amount: float
    quote_amount: float
    entry_price: float
    last_update: datetime

@dataclass
class OrderBookState:
    best_bid: float
    best_ask: float
    bid_volume: float
    ask_volume: float
    spread: float
    mid_price: float

class TradingStrategy:
    """Implements pure market making strategy with risk management."""
    
    def __init__(self):
        # Strategy parameters
        self.min_spread = float(os.getenv("MIN_SPREAD", "0.001"))
        self.max_spread = float(os.getenv("MAX_SPREAD", "0.05"))
        self.max_position_size = float(os.getenv("MAX_POSITION_SIZE", "100"))
        self.rebalance_threshold = float(os.getenv("REBALANCE_THRESHOLD", "0.2"))
        
        # Risk parameters
        self.max_drawdown = float(os.getenv("MAX_DRAWDOWN", "0.1"))
        self.max_leverage = float(os.getenv("MAX_LEVERAGE", "1.0"))
        self.min_liquidity = float(os.getenv("MIN_LIQUIDITY", "10000"))
        
        # Position tracking
        self.position = Position(0.0, 0.0, 0.0, datetime.utcnow())
        self.initial_balance = None
        
        # Performance tracking
        self.total_pnl = 0.0
        self.win_count = 0
        self.total_trades = 0
        
        # Volatility tracking
        self.price_history = []
        self.volatility_window = 30  # 30 periods
        
    def calculate_parameters(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate trading parameters based on market data.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Dictionary containing calculated parameters
        """
        try:
            # Calculate order book state
            order_book = market_data["order_book"]
            ob_state = self._calculate_order_book_state(order_book)
            
            # Calculate volatility
            volatility = self._calculate_volatility(market_data["price"])
            
            # Calculate position skew
            position_skew = self._calculate_position_skew()
            
            # Calculate spreads
            bid_spread = self._calculate_bid_spread(ob_state, volatility, position_skew)
            ask_spread = self._calculate_ask_spread(ob_state, volatility, position_skew)
            
            # Calculate order sizes
            bid_size = self._calculate_order_size("bid", ob_state, position_skew)
            ask_size = self._calculate_order_size("ask", ob_state, position_skew)
            
            # Check risk limits
            if not self._check_risk_limits(market_data):
                logger.warning("Risk limits exceeded, reducing position sizes")
                bid_size *= 0.5
                ask_size *= 0.5
            
            return {
                "bid_price": ob_state.mid_price * (1 - bid_spread),
                "ask_price": ob_state.mid_price * (1 + ask_spread),
                "bid_size": bid_size,
                "ask_size": ask_size,
                "volatility": volatility,
                "position_skew": position_skew,
                "spread": ob_state.spread,
                "mid_price": ob_state.mid_price
            }
            
        except Exception as e:
            logger.error(f"Error calculating parameters: {str(e)}")
            return {}
    
    def _calculate_order_book_state(self, order_book: Dict) -> OrderBookState:
        """Calculate order book state."""
        bids = order_book["bids"]
        asks = order_book["asks"]
        
        if not bids or not asks:
            raise ValueError("Empty order book")
            
        best_bid = max(bid["price"] for bid in bids)
        best_ask = min(ask["price"] for ask in asks)
        
        bid_volume = sum(bid["size"] for bid in bids)
        ask_volume = sum(ask["size"] for ask in asks)
        
        spread = (best_ask - best_bid) / best_bid
        mid_price = (best_bid + best_ask) / 2
        
        return OrderBookState(
            best_bid=best_bid,
            best_ask=best_ask,
            bid_volume=bid_volume,
            ask_volume=ask_volume,
            spread=spread,
            mid_price=mid_price
        )
    
    def _calculate_volatility(self, current_price: float) -> float:
        """Calculate price volatility."""
        self.price_history.append(current_price)
        if len(self.price_history) > self.volatility_window:
            self.price_history.pop(0)
            
        if len(self.price_history) < 2:
            return 0.0
            
        returns = np.diff(np.log(self.price_history))
        return np.std(returns) * np.sqrt(252)  # Annualized volatility
    
    def _calculate_position_skew(self) -> float:
        """Calculate position skew for inventory management."""
        if self.position.base_amount == 0:
            return 0.0
            
        total_value = (self.position.base_amount * self.position.entry_price +
                      self.position.quote_amount)
        base_value = self.position.base_amount * self.position.entry_price
        
        return (base_value / total_value) - 0.5  # Target 50% base
    
    def _calculate_bid_spread(self, ob_state: OrderBookState,
                            volatility: float, position_skew: float) -> float:
        """Calculate bid spread based on market conditions."""
        base_spread = max(self.min_spread, min(self.max_spread, ob_state.spread))
        
        # Adjust for volatility
        vol_adjustment = volatility * 0.1  # 10% of volatility
        
        # Adjust for position skew
        skew_adjustment = position_skew * 0.001  # 0.1% per skew unit
        
        return base_spread + vol_adjustment + skew_adjustment
    
    def _calculate_ask_spread(self, ob_state: OrderBookState,
                            volatility: float, position_skew: float) -> float:
        """Calculate ask spread based on market conditions."""
        base_spread = max(self.min_spread, min(self.max_spread, ob_state.spread))
        
        # Adjust for volatility
        vol_adjustment = volatility * 0.1  # 10% of volatility
        
        # Adjust for position skew (opposite of bid)
        skew_adjustment = -position_skew * 0.001  # 0.1% per skew unit
        
        return base_spread + vol_adjustment + skew_adjustment
    
    def _calculate_order_size(self, side: str, ob_state: OrderBookState,
                            position_skew: float) -> float:
        """Calculate order size based on market conditions and position."""
        # Base size
        base_size = self.max_position_size * 0.1  # 10% of max position
        
        # Adjust for liquidity
        if side == "bid":
            liquidity_factor = min(1.0, ob_state.bid_volume / self.min_liquidity)
        else:
            liquidity_factor = min(1.0, ob_state.ask_volume / self.min_liquidity)
            
        # Adjust for position skew
        if side == "bid":
            skew_factor = 1.0 - position_skew
        else:
            skew_factor = 1.0 + position_skew
            
        return base_size * liquidity_factor * skew_factor
    
    def _check_risk_limits(self, market_data: Dict[str, Any]) -> bool:
        """Check if current position is within risk limits."""
        # Check drawdown
        if self.initial_balance is None:
            self.initial_balance = (self.position.base_amount * market_data["price"] +
                                  self.position.quote_amount)
            return True
            
        current_value = (self.position.base_amount * market_data["price"] +
                        self.position.quote_amount)
        drawdown = (self.initial_balance - current_value) / self.initial_balance
        
        if drawdown > self.max_drawdown:
            logger.warning(f"Drawdown limit exceeded: {drawdown:.2%}")
            return False
            
        # Check leverage
        leverage = abs(self.position.base_amount * market_data["price"] / current_value)
        if leverage > self.max_leverage:
            logger.warning(f"Leverage limit exceeded: {leverage:.2f}x")
            return False
            
        return True
    
    def update_position(self, trade: Dict[str, Any]):
        """Update position after a trade."""
        price = trade["price"]
        size = trade["size"]
        side = trade["side"]
        
        if side == "buy":
            self.position.base_amount += size
            self.position.quote_amount -= size * price
        else:
            self.position.base_amount -= size
            self.position.quote_amount += size * price
            
        self.position.entry_price = price
        self.position.last_update = datetime.utcnow()
        
        # Update performance metrics
        self.total_trades += 1
        if (side == "buy" and price < self.position.entry_price) or \
           (side == "sell" and price > self.position.entry_price):
            self.win_count += 1
            
        self.total_pnl = (self.position.base_amount * price +
                         self.position.quote_amount - self.initial_balance)
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics."""
        return {
            "total_pnl": self.total_pnl,
            "win_rate": self.win_count / self.total_trades if self.total_trades > 0 else 0.0,
            "position_size": self.position.base_amount,
            "position_value": self.position.base_amount * self.position.entry_price,
            "quote_balance": self.position.quote_amount
        } 