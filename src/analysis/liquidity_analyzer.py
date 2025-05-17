"""
Liquidity analyzer that implements various liquidity analysis methods.
"""
import logging
import numpy as np
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)

class LiquidityAnalyzer(BaseAnalyzer):
    """Liquidity analysis implementation."""
    
    def __init__(self):
        super().__init__()
        self.required_fields = [
            'order_book',
            'trades',
            'liquidity_pools',
            'price',
            'volume_24h'
        ]
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform liquidity analysis on market data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing liquidity analysis results
        """
        if not self._validate_data(data, self.required_fields):
            logger.error(f"Missing required fields for liquidity analysis: {self.required_fields}")
            return {}
            
        try:
            # Extract liquidity data
            order_book = data['order_book']
            trades = data['trades']
            liquidity_pools = data['liquidity_pools']
            price = data['price']
            volume_24h = data['volume_24h']
            
            # Calculate liquidity metrics
            depth = self._calculate_market_depth(order_book)
            spread = self._calculate_spread(order_book)
            slippage = self._calculate_slippage(trades)
            pool_metrics = self._calculate_pool_metrics(liquidity_pools)
            
            # Calculate overall liquidity health
            liquidity_health = self._calculate_liquidity_health(
                depth,
                spread,
                slippage,
                pool_metrics,
                volume_24h
            )
            
            # Generate signals
            signals = self._generate_signals(
                depth,
                spread,
                slippage,
                pool_metrics,
                liquidity_health
            )
            
            # Calculate confidence
            confidence_factors = {
                'depth': min(depth['total'] / 1e6, 1),  # Normalize to 1M USD
                'spread': 1 - min(spread / 0.01, 1),  # Normalize to 1% spread
                'slippage': 1 - min(slippage / 0.01, 1),  # Normalize to 1% slippage
                'pool_liquidity': min(pool_metrics['total_liquidity'] / 1e6, 1),  # Normalize to 1M USD
                'volume': min(volume_24h / 1e6, 1)  # Normalize to 1M USD
            }
            
            self.confidence = self._calculate_confidence(confidence_factors)
            
            results = {
                'liquidity_health': liquidity_health,
                'signals': signals,
                'metrics': {
                    'depth': depth,
                    'spread': spread,
                    'slippage': slippage,
                    'pool_metrics': pool_metrics
                },
                'confidence': self.confidence
            }
            
            self._log_analysis(results)
            return results
            
        except Exception as e:
            logger.error(f"Error in liquidity analysis: {str(e)}")
            return {}
    
    def _calculate_market_depth(self, order_book: Dict[str, List[Dict[str, float]]]) -> Dict[str, float]:
        """
        Calculate market depth at different levels.
        
        Args:
            order_book: Dictionary containing bid and ask orders
            
        Returns:
            Dictionary containing depth metrics
        """
        bids = order_book['bids']
        asks = order_book['asks']
        
        # Calculate depth at different levels
        levels = [0.1, 0.5, 1.0, 2.0, 5.0]  # Percentage from mid price
        depth = {
            'bids': {},
            'asks': {},
            'total': 0.0
        }
        
        mid_price = (bids[0]['price'] + asks[0]['price']) / 2
        
        for level in levels:
            bid_depth = sum(order['size'] * order['price'] 
                          for order in bids 
                          if order['price'] >= mid_price * (1 - level/100))
            ask_depth = sum(order['size'] * order['price'] 
                          for order in asks 
                          if order['price'] <= mid_price * (1 + level/100))
            
            depth['bids'][level] = bid_depth
            depth['asks'][level] = ask_depth
            
        depth['total'] = sum(depth['bids'].values()) + sum(depth['asks'].values())
        return depth
    
    def _calculate_spread(self, order_book: Dict[str, List[Dict[str, float]]]) -> float:
        """
        Calculate current market spread.
        
        Args:
            order_book: Dictionary containing bid and ask orders
            
        Returns:
            Spread as a percentage
        """
        if not order_book['bids'] or not order_book['asks']:
            return float('inf')
            
        best_bid = order_book['bids'][0]['price']
        best_ask = order_book['asks'][0]['price']
        
        return (best_ask - best_bid) / best_bid * 100
    
    def _calculate_slippage(self, trades: List[Dict[str, Any]]) -> float:
        """
        Calculate average slippage from recent trades.
        
        Args:
            trades: List of recent trades
            
        Returns:
            Average slippage as a percentage
        """
        if not trades:
            return 0.0
            
        slippages = []
        for trade in trades:
            if 'expected_price' in trade and 'executed_price' in trade:
                slippage = abs(trade['executed_price'] - trade['expected_price']) / trade['expected_price'] * 100
                slippages.append(slippage)
                
        return np.mean(slippages) if slippages else 0.0
    
    def _calculate_pool_metrics(self, pools: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate metrics for liquidity pools.
        
        Args:
            pools: List of liquidity pools
            
        Returns:
            Dictionary containing pool metrics
        """
        if not pools:
            return {
                'total_liquidity': 0.0,
                'avg_apy': 0.0,
                'utilization': 0.0
            }
            
        total_liquidity = sum(pool['liquidity'] for pool in pools)
        avg_apy = np.mean([pool['apy'] for pool in pools])
        utilization = np.mean([pool['utilization'] for pool in pools])
        
        return {
            'total_liquidity': total_liquidity,
            'avg_apy': avg_apy,
            'utilization': utilization
        }
    
    def _calculate_liquidity_health(self, depth: Dict[str, float], spread: float,
                                  slippage: float, pool_metrics: Dict[str, float],
                                  volume_24h: float) -> str:
        """
        Calculate overall liquidity health.
        
        Args:
            depth: Market depth metrics
            spread: Current market spread
            slippage: Average slippage
            pool_metrics: Liquidity pool metrics
            volume_24h: 24-hour trading volume
            
        Returns:
            Liquidity health status
        """
        # Define thresholds
        depth_threshold = 1e6  # 1M USD
        spread_threshold = 0.5  # 0.5%
        slippage_threshold = 0.5  # 0.5%
        pool_liquidity_threshold = 1e6  # 1M USD
        volume_threshold = 1e6  # 1M USD
        
        # Count positive indicators
        positive_indicators = 0
        if depth['total'] > depth_threshold:
            positive_indicators += 1
        if spread < spread_threshold:
            positive_indicators += 1
        if slippage < slippage_threshold:
            positive_indicators += 1
        if pool_metrics['total_liquidity'] > pool_liquidity_threshold:
            positive_indicators += 1
        if volume_24h > volume_threshold:
            positive_indicators += 1
            
        # Determine liquidity health
        if positive_indicators >= 4:
            return "excellent"
        elif positive_indicators >= 3:
            return "good"
        elif positive_indicators >= 2:
            return "moderate"
        else:
            return "poor"
    
    def _generate_signals(self, depth: Dict[str, float], spread: float,
                         slippage: float, pool_metrics: Dict[str, float],
                         liquidity_health: str) -> Dict[str, float]:
        """
        Generate trading signals based on liquidity analysis.
        
        Args:
            depth: Market depth metrics
            spread: Current market spread
            slippage: Average slippage
            pool_metrics: Liquidity pool metrics
            liquidity_health: Liquidity health status
            
        Returns:
            Dictionary of trading signals
        """
        signals = {
            'depth_signal': 0.0,
            'spread_signal': 0.0,
            'slippage_signal': 0.0,
            'pool_signal': 0.0,
            'overall_signal': 0.0
        }
        
        # Depth signal
        if depth['total'] > 1e6:
            signals['depth_signal'] = 1.0
        elif depth['total'] > 5e5:
            signals['depth_signal'] = 0.5
        else:
            signals['depth_signal'] = -1.0
            
        # Spread signal
        if spread < 0.1:
            signals['spread_signal'] = 1.0
        elif spread < 0.5:
            signals['spread_signal'] = 0.5
        else:
            signals['spread_signal'] = -1.0
            
        # Slippage signal
        if slippage < 0.1:
            signals['slippage_signal'] = 1.0
        elif slippage < 0.5:
            signals['slippage_signal'] = 0.5
        else:
            signals['slippage_signal'] = -1.0
            
        # Pool signal
        if pool_metrics['total_liquidity'] > 1e6:
            signals['pool_signal'] = 1.0
        elif pool_metrics['total_liquidity'] > 5e5:
            signals['pool_signal'] = 0.5
        else:
            signals['pool_signal'] = -1.0
            
        # Overall signal based on liquidity health
        if liquidity_health == "excellent":
            signals['overall_signal'] = 1.0
        elif liquidity_health == "good":
            signals['overall_signal'] = 0.5
        elif liquidity_health == "moderate":
            signals['overall_signal'] = 0.0
        else:
            signals['overall_signal'] = -1.0
            
        return signals 