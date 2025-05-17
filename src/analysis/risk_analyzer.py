"""
Risk analyzer that implements various risk analysis methods.
"""
import logging
import numpy as np
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)

class RiskAnalyzer(BaseAnalyzer):
    """Risk analysis implementation."""
    
    def __init__(self):
        super().__init__()
        self.required_fields = [
            'prices',
            'volumes',
            'order_book',
            'trades',
            'liquidity_pools',
            'market_cap',
            'volume_24h'
        ]
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform risk analysis on market data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing risk analysis results
        """
        if not self._validate_data(data, self.required_fields):
            logger.error(f"Missing required fields for risk analysis: {self.required_fields}")
            return {}
            
        try:
            # Extract risk data
            prices = np.array(data['prices'])
            volumes = np.array(data['volumes'])
            order_book = data['order_book']
            trades = data['trades']
            liquidity_pools = data['liquidity_pools']
            market_cap = data['market_cap']
            volume_24h = data['volume_24h']
            
            # Calculate risk metrics
            volatility = self._calculate_volatility(prices)
            drawdown = self._calculate_drawdown(prices)
            liquidity_risk = self._calculate_liquidity_risk(order_book, trades)
            concentration_risk = self._calculate_concentration_risk(liquidity_pools)
            market_risk = self._calculate_market_risk(market_cap, volume_24h)
            
            # Calculate overall risk level
            risk_level = self._calculate_risk_level(
                volatility,
                drawdown,
                liquidity_risk,
                concentration_risk,
                market_risk
            )
            
            # Generate signals
            signals = self._generate_signals(
                volatility,
                drawdown,
                liquidity_risk,
                concentration_risk,
                market_risk,
                risk_level
            )
            
            # Calculate confidence
            confidence_factors = {
                'volatility': 1 - min(volatility / 0.1, 1),  # Normalize to 10% volatility
                'drawdown': 1 - min(drawdown / 0.2, 1),  # Normalize to 20% drawdown
                'liquidity': 1 - min(liquidity_risk / 0.5, 1),  # Normalize to 50% liquidity risk
                'concentration': 1 - min(concentration_risk / 0.7, 1),  # Normalize to 70% concentration
                'market': 1 - min(market_risk / 0.5, 1)  # Normalize to 50% market risk
            }
            
            self.confidence = self._calculate_confidence(confidence_factors)
            
            results = {
                'risk_level': risk_level,
                'signals': signals,
                'metrics': {
                    'volatility': volatility,
                    'drawdown': drawdown,
                    'liquidity_risk': liquidity_risk,
                    'concentration_risk': concentration_risk,
                    'market_risk': market_risk
                },
                'confidence': self.confidence
            }
            
            self._log_analysis(results)
            return results
            
        except Exception as e:
            logger.error(f"Error in risk analysis: {str(e)}")
            return {}
    
    def _calculate_volatility(self, prices: np.ndarray, window: int = 20) -> float:
        """
        Calculate price volatility.
        
        Args:
            prices: Array of historical prices
            window: Rolling window size
            
        Returns:
            Volatility as a percentage
        """
        if len(prices) < 2:
            return 0.0
            
        returns = np.diff(prices) / prices[:-1]
        return np.std(returns[-window:]) * 100
    
    def _calculate_drawdown(self, prices: np.ndarray) -> float:
        """
        Calculate maximum drawdown.
        
        Args:
            prices: Array of historical prices
            
        Returns:
            Maximum drawdown as a percentage
        """
        if len(prices) < 2:
            return 0.0
            
        peak = np.maximum.accumulate(prices)
        drawdown = (peak - prices) / peak
        return np.max(drawdown) * 100
    
    def _calculate_liquidity_risk(self, order_book: Dict[str, List[Dict[str, float]]],
                                trades: List[Dict[str, Any]]) -> float:
        """
        Calculate liquidity risk score.
        
        Args:
            order_book: Dictionary containing bid and ask orders
            trades: List of recent trades
            
        Returns:
            Liquidity risk score between 0 and 1
        """
        if not order_book['bids'] or not order_book['asks']:
            return 1.0
            
        # Calculate bid-ask spread
        best_bid = order_book['bids'][0]['price']
        best_ask = order_book['asks'][0]['price']
        spread = (best_ask - best_bid) / best_bid
        
        # Calculate order book depth
        bid_depth = sum(order['size'] * order['price'] for order in order_book['bids'])
        ask_depth = sum(order['size'] * order['price'] for order in order_book['asks'])
        total_depth = bid_depth + ask_depth
        
        # Calculate trade frequency
        trade_frequency = len(trades) / 24  # trades per hour
        
        # Combine factors
        spread_risk = min(spread / 0.01, 1)  # Normalize to 1% spread
        depth_risk = 1 - min(total_depth / 1e6, 1)  # Normalize to 1M USD
        frequency_risk = 1 - min(trade_frequency / 100, 1)  # Normalize to 100 trades/hour
        
        return (spread_risk * 0.4 + depth_risk * 0.4 + frequency_risk * 0.2)
    
    def _calculate_concentration_risk(self, pools: List[Dict[str, Any]]) -> float:
        """
        Calculate concentration risk score.
        
        Args:
            pools: List of liquidity pools
            
        Returns:
            Concentration risk score between 0 and 1
        """
        if not pools:
            return 1.0
            
        # Calculate total liquidity
        total_liquidity = sum(pool['liquidity'] for pool in pools)
        
        # Calculate concentration using Gini coefficient
        pool_sizes = sorted([pool['liquidity'] for pool in pools])
        n = len(pool_sizes)
        
        if n == 0 or total_liquidity == 0:
            return 1.0
            
        index = np.arange(1, n + 1)
        gini = ((2 * index - n - 1) * pool_sizes).sum() / (n * sum(pool_sizes))
        
        return gini
    
    def _calculate_market_risk(self, market_cap: float, volume_24h: float) -> float:
        """
        Calculate market risk score.
        
        Args:
            market_cap: Market capitalization
            volume_24h: 24-hour trading volume
            
        Returns:
            Market risk score between 0 and 1
        """
        if market_cap == 0:
            return 1.0
            
        # Calculate volume to market cap ratio
        volume_ratio = volume_24h / market_cap
        
        # Define risk thresholds
        if market_cap < 1e6:  # Less than 1M USD
            cap_risk = 1.0
        elif market_cap < 1e7:  # Less than 10M USD
            cap_risk = 0.8
        elif market_cap < 1e8:  # Less than 100M USD
            cap_risk = 0.6
        elif market_cap < 1e9:  # Less than 1B USD
            cap_risk = 0.4
        else:
            cap_risk = 0.2
            
        # Volume risk
        if volume_ratio < 0.01:  # Less than 1% daily volume
            volume_risk = 1.0
        elif volume_ratio < 0.05:  # Less than 5% daily volume
            volume_risk = 0.8
        elif volume_ratio < 0.1:  # Less than 10% daily volume
            volume_risk = 0.6
        elif volume_ratio < 0.2:  # Less than 20% daily volume
            volume_risk = 0.4
        else:
            volume_risk = 0.2
            
        return (cap_risk * 0.6 + volume_risk * 0.4)
    
    def _calculate_risk_level(self, volatility: float, drawdown: float,
                            liquidity_risk: float, concentration_risk: float,
                            market_risk: float) -> str:
        """
        Calculate overall risk level.
        
        Args:
            volatility: Price volatility
            drawdown: Maximum drawdown
            liquidity_risk: Liquidity risk score
            concentration_risk: Concentration risk score
            market_risk: Market risk score
            
        Returns:
            Risk level status
        """
        # Define thresholds
        volatility_threshold = 50  # 50% annualized volatility
        drawdown_threshold = 30  # 30% maximum drawdown
        liquidity_threshold = 0.7  # 70% liquidity risk
        concentration_threshold = 0.8  # 80% concentration risk
        market_threshold = 0.7  # 70% market risk
        
        # Count risk indicators
        risk_indicators = 0
        if volatility > volatility_threshold:
            risk_indicators += 1
        if drawdown > drawdown_threshold:
            risk_indicators += 1
        if liquidity_risk > liquidity_threshold:
            risk_indicators += 1
        if concentration_risk > concentration_threshold:
            risk_indicators += 1
        if market_risk > market_threshold:
            risk_indicators += 1
            
        # Determine risk level
        if risk_indicators >= 4:
            return "extreme"
        elif risk_indicators >= 3:
            return "high"
        elif risk_indicators >= 2:
            return "moderate"
        else:
            return "low"
    
    def _generate_signals(self, volatility: float, drawdown: float,
                         liquidity_risk: float, concentration_risk: float,
                         market_risk: float, risk_level: str) -> Dict[str, float]:
        """
        Generate trading signals based on risk analysis.
        
        Args:
            volatility: Price volatility
            drawdown: Maximum drawdown
            liquidity_risk: Liquidity risk score
            concentration_risk: Concentration risk score
            market_risk: Market risk score
            risk_level: Overall risk level
            
        Returns:
            Dictionary of trading signals
        """
        signals = {
            'volatility_signal': 0.0,
            'drawdown_signal': 0.0,
            'liquidity_signal': 0.0,
            'concentration_signal': 0.0,
            'market_signal': 0.0,
            'overall_signal': 0.0
        }
        
        # Volatility signal
        if volatility > 50:
            signals['volatility_signal'] = -1.0
        elif volatility > 30:
            signals['volatility_signal'] = -0.5
        else:
            signals['volatility_signal'] = 0.0
            
        # Drawdown signal
        if drawdown > 30:
            signals['drawdown_signal'] = -1.0
        elif drawdown > 20:
            signals['drawdown_signal'] = -0.5
        else:
            signals['drawdown_signal'] = 0.0
            
        # Liquidity signal
        if liquidity_risk > 0.7:
            signals['liquidity_signal'] = -1.0
        elif liquidity_risk > 0.5:
            signals['liquidity_signal'] = -0.5
        else:
            signals['liquidity_signal'] = 0.0
            
        # Concentration signal
        if concentration_risk > 0.8:
            signals['concentration_signal'] = -1.0
        elif concentration_risk > 0.6:
            signals['concentration_signal'] = -0.5
        else:
            signals['concentration_signal'] = 0.0
            
        # Market signal
        if market_risk > 0.7:
            signals['market_signal'] = -1.0
        elif market_risk > 0.5:
            signals['market_signal'] = -0.5
        else:
            signals['market_signal'] = 0.0
            
        # Overall signal based on risk level
        if risk_level == "extreme":
            signals['overall_signal'] = -1.0
        elif risk_level == "high":
            signals['overall_signal'] = -0.5
        elif risk_level == "moderate":
            signals['overall_signal'] = 0.0
        else:
            signals['overall_signal'] = 0.5
            
        return signals 