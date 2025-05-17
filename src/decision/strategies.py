"""
Trading strategy implementations for the decision engine.
"""
import logging
from typing import Dict, List, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Strategy(ABC):
    """Base class for all trading strategies."""
    
    def __init__(self):
        self.name = self.__class__.__name__.lower()
    
    @abstractmethod
    async def evaluate(self, analysis: Dict[str, Any],
                      current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate strategy based on analysis and current state."""
        pass
    
    @abstractmethod
    async def generate_actions(self, analysis: Dict[str, Any],
                             current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate trading actions based on evaluation."""
        pass

class MarketMakingStrategy(Strategy):
    """Market making strategy implementation."""
    
    def __init__(self):
        super().__init__()
        self.min_spread = 0.001  # 0.1% minimum spread
        self.max_position = 100  # Maximum position size
        self.rebalance_threshold = 0.2  # Rebalance when position exceeds 20% of max
    
    async def evaluate(self, analysis: Dict[str, Any],
                      current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate market making opportunities."""
        try:
            # Calculate base score
            score = 0.0
            
            # Check market regime
            if analysis.get('market_regime') == 'normal':
                score += 0.4
            elif analysis.get('market_regime') == 'volatile':
                score += 0.2
            
            # Check liquidity
            liquidity_score = min(1.0, current_state.get('liquidity', 0) / 1000000)
            score += liquidity_score * 0.3
            
            # Check volatility
            volatility = analysis.get('volatility', 0)
            if 0.001 <= volatility <= 0.05:  # Ideal volatility range
                score += 0.3
            elif volatility > 0.05:  # Too volatile
                score -= 0.2
            
            return {
                'score': max(0.0, min(1.0, score)),
                'market_regime': analysis.get('market_regime', 'unknown'),
                'liquidity': liquidity_score,
                'volatility': volatility
            }
            
        except Exception as e:
            logger.error(f"Error in market making evaluation: {e}")
            return {'score': 0.0}
    
    async def generate_actions(self, analysis: Dict[str, Any],
                             current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate market making actions."""
        try:
            actions = []
            current_price = current_state.get('current_price', 0)
            current_position = current_state.get('position_size', 0)
            
            # Calculate spread
            volatility = analysis.get('volatility', 0)
            spread = max(self.min_spread, volatility * 2)
            
            # Calculate order sizes
            base_size = self.max_position * (1 - abs(current_position) / self.max_position)
            
            # Generate buy order
            if current_position < self.max_position:
                buy_price = current_price * (1 - spread/2)
                buy_size = min(base_size, self.max_position - current_position)
                
                actions.append({
                    'type': 'buy',
                    'price': buy_price,
                    'size': buy_size,
                    'reason': 'market_making'
                })
            
            # Generate sell order
            if current_position > -self.max_position:
                sell_price = current_price * (1 + spread/2)
                sell_size = min(base_size, self.max_position + current_position)
                
                actions.append({
                    'type': 'sell',
                    'price': sell_price,
                    'size': sell_size,
                    'reason': 'market_making'
                })
            
            # Check if rebalancing is needed
            if abs(current_position) > self.max_position * self.rebalance_threshold:
                rebalance_size = -current_position * 0.5  # Rebalance half of the position
                
                actions.append({
                    'type': 'rebalance',
                    'size': rebalance_size,
                    'reason': 'position_management'
                })
            
            return actions
            
        except Exception as e:
            logger.error(f"Error in market making action generation: {e}")
            return []

class ArbitrageStrategy(Strategy):
    """Arbitrage strategy implementation."""
    
    def __init__(self):
        super().__init__()
        self.min_profit_threshold = 0.002  # 0.2% minimum profit
        self.max_slippage = 0.001  # 0.1% maximum slippage
        self.max_position = 50  # Maximum position size
    
    async def evaluate(self, analysis: Dict[str, Any],
                      current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate arbitrage opportunities."""
        try:
            # Calculate base score
            score = 0.0
            
            # Check market regime
            if analysis.get('market_regime') == 'normal':
                score += 0.3
            elif analysis.get('market_regime') == 'volatile':
                score += 0.4  # More opportunities in volatile markets
            
            # Check price discrepancies
            price_discrepancy = analysis.get('price_discrepancy', 0)
            if price_discrepancy > self.min_profit_threshold:
                score += min(1.0, price_discrepancy * 10) * 0.4
            
            # Check liquidity
            liquidity_score = min(1.0, current_state.get('liquidity', 0) / 500000)
            score += liquidity_score * 0.3
            
            return {
                'score': max(0.0, min(1.0, score)),
                'market_regime': analysis.get('market_regime', 'unknown'),
                'price_discrepancy': price_discrepancy,
                'liquidity': liquidity_score
            }
            
        except Exception as e:
            logger.error(f"Error in arbitrage evaluation: {e}")
            return {'score': 0.0}
    
    async def generate_actions(self, analysis: Dict[str, Any],
                             current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate arbitrage actions."""
        try:
            actions = []
            price_discrepancy = analysis.get('price_discrepancy', 0)
            
            if price_discrepancy > self.min_profit_threshold:
                # Calculate position size based on liquidity and profit potential
                liquidity = current_state.get('liquidity', 0)
                position_size = min(
                    self.max_position,
                    liquidity * 0.1,  # Use up to 10% of available liquidity
                    price_discrepancy * 1000  # Scale with profit potential
                )
                
                # Generate arbitrage action
                actions.append({
                    'type': 'arbitrage',
                    'size': position_size,
                    'expected_profit': price_discrepancy,
                    'max_slippage': self.max_slippage,
                    'reason': 'price_discrepancy'
                })
            
            return actions
            
        except Exception as e:
            logger.error(f"Error in arbitrage action generation: {e}")
            return []

class LiquidityStrategy(Strategy):
    """Liquidity provision strategy implementation."""
    
    def __init__(self):
        super().__init__()
        self.min_liquidity_threshold = 10000  # Minimum liquidity to provide
        self.max_position = 200  # Maximum position size
        self.rebalance_threshold = 0.3  # Rebalance when position exceeds 30% of max
    
    async def evaluate(self, analysis: Dict[str, Any],
                      current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate liquidity provision opportunities."""
        try:
            # Calculate base score
            score = 0.0
            
            # Check market regime
            if analysis.get('market_regime') == 'normal':
                score += 0.3
            elif analysis.get('market_regime') == 'volatile':
                score += 0.2
            
            # Check liquidity needs
            current_liquidity = current_state.get('liquidity', 0)
            if current_liquidity < self.min_liquidity_threshold:
                score += min(1.0, (self.min_liquidity_threshold - current_liquidity) / self.min_liquidity_threshold) * 0.4
            
            # Check volatility
            volatility = analysis.get('volatility', 0)
            if volatility > 0.05:  # High volatility means more liquidity needed
                score += 0.3
            
            return {
                'score': max(0.0, min(1.0, score)),
                'market_regime': analysis.get('market_regime', 'unknown'),
                'liquidity_needed': current_liquidity < self.min_liquidity_threshold,
                'volatility': volatility
            }
            
        except Exception as e:
            logger.error(f"Error in liquidity evaluation: {e}")
            return {'score': 0.0}
    
    async def generate_actions(self, analysis: Dict[str, Any],
                             current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate liquidity provision actions."""
        try:
            actions = []
            current_liquidity = current_state.get('liquidity', 0)
            current_position = current_state.get('position_size', 0)
            
            if current_liquidity < self.min_liquidity_threshold:
                # Calculate position size based on liquidity gap
                liquidity_gap = self.min_liquidity_threshold - current_liquidity
                position_size = min(
                    self.max_position,
                    liquidity_gap * 0.5  # Provide 50% of the liquidity gap
                )
                
                # Generate liquidity provision action
                actions.append({
                    'type': 'provide_liquidity',
                    'size': position_size,
                    'reason': 'liquidity_gap'
                })
            
            # Check if rebalancing is needed
            if abs(current_position) > self.max_position * self.rebalance_threshold:
                rebalance_size = -current_position * 0.5  # Rebalance half of the position
                
                actions.append({
                    'type': 'rebalance',
                    'size': rebalance_size,
                    'reason': 'position_management'
                })
            
            return actions
            
        except Exception as e:
            logger.error(f"Error in liquidity action generation: {e}")
            return [] 