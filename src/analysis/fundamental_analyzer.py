"""
Fundamental analyzer that implements various fundamental analysis methods.
"""
import logging
import numpy as np
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)

class FundamentalAnalyzer(BaseAnalyzer):
    """Fundamental analysis implementation."""
    
    def __init__(self):
        super().__init__()
        self.required_fields = [
            'market_cap',
            'volume_24h',
            'total_supply',
            'circulating_supply',
            'price',
            'liquidity',
            'holders',
            'transactions_24h'
        ]
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform fundamental analysis on market data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing fundamental analysis results
        """
        if not self._validate_data(data, self.required_fields):
            logger.error(f"Missing required fields for fundamental analysis: {self.required_fields}")
            return {}
            
        try:
            # Calculate fundamental metrics
            market_cap = data['market_cap']
            volume_24h = data['volume_24h']
            total_supply = data['total_supply']
            circulating_supply = data['circulating_supply']
            price = data['price']
            liquidity = data['liquidity']
            holders = data['holders']
            transactions_24h = data['transactions_24h']
            
            # Calculate key ratios
            volume_market_cap_ratio = volume_24h / market_cap if market_cap > 0 else 0
            liquidity_market_cap_ratio = liquidity / market_cap if market_cap > 0 else 0
            circulating_ratio = circulating_supply / total_supply if total_supply > 0 else 0
            
            # Calculate network metrics
            avg_transaction_value = volume_24h / transactions_24h if transactions_24h > 0 else 0
            holder_concentration = self._calculate_holder_concentration(holders)
            
            # Calculate market health indicators
            market_health = self._calculate_market_health(
                volume_market_cap_ratio,
                liquidity_market_cap_ratio,
                circulating_ratio,
                holder_concentration
            )
            
            # Generate signals
            signals = self._generate_signals(
                volume_market_cap_ratio,
                liquidity_market_cap_ratio,
                circulating_ratio,
                holder_concentration,
                market_health
            )
            
            # Calculate confidence
            confidence_factors = {
                'market_cap': min(market_cap / 1e9, 1),  # Normalize to billions
                'liquidity': min(liquidity / market_cap, 1) if market_cap > 0 else 0,
                'volume': min(volume_24h / market_cap, 1) if market_cap > 0 else 0,
                'holders': min(holders / 10000, 1)  # Normalize to 10k holders
            }
            
            self.confidence = self._calculate_confidence(confidence_factors)
            
            results = {
                'market_health': market_health,
                'signals': signals,
                'metrics': {
                    'volume_market_cap_ratio': volume_market_cap_ratio,
                    'liquidity_market_cap_ratio': liquidity_market_cap_ratio,
                    'circulating_ratio': circulating_ratio,
                    'holder_concentration': holder_concentration,
                    'avg_transaction_value': avg_transaction_value
                },
                'confidence': self.confidence
            }
            
            self._log_analysis(results)
            return results
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis: {str(e)}")
            return {}
    
    def _calculate_holder_concentration(self, holders: Dict[str, int]) -> float:
        """
        Calculate holder concentration using Gini coefficient.
        
        Args:
            holders: Dictionary of holder addresses and their balances
            
        Returns:
            Holder concentration score between 0 and 1
        """
        if not holders:
            return 1.0
            
        balances = sorted(holders.values())
        n = len(balances)
        if n == 0:
            return 1.0
            
        # Calculate Gini coefficient
        index = np.arange(1, n + 1)
        return ((2 * index - n - 1) * balances).sum() / (n * sum(balances))
    
    def _calculate_market_health(self, volume_ratio: float, liquidity_ratio: float,
                               circulating_ratio: float, holder_concentration: float) -> str:
        """
        Calculate overall market health based on fundamental metrics.
        
        Args:
            volume_ratio: Volume to market cap ratio
            liquidity_ratio: Liquidity to market cap ratio
            circulating_ratio: Circulating supply ratio
            holder_concentration: Holder concentration score
            
        Returns:
            Market health status
        """
        # Define thresholds
        volume_threshold = 0.1
        liquidity_threshold = 0.05
        circulating_threshold = 0.7
        concentration_threshold = 0.7
        
        # Count positive indicators
        positive_indicators = 0
        if volume_ratio > volume_threshold:
            positive_indicators += 1
        if liquidity_ratio > liquidity_threshold:
            positive_indicators += 1
        if circulating_ratio > circulating_threshold:
            positive_indicators += 1
        if holder_concentration < concentration_threshold:
            positive_indicators += 1
            
        # Determine market health
        if positive_indicators >= 3:
            return "healthy"
        elif positive_indicators >= 2:
            return "moderate"
        else:
            return "risky"
    
    def _generate_signals(self, volume_ratio: float, liquidity_ratio: float,
                         circulating_ratio: float, holder_concentration: float,
                         market_health: str) -> Dict[str, float]:
        """
        Generate trading signals based on fundamental metrics.
        
        Args:
            volume_ratio: Volume to market cap ratio
            liquidity_ratio: Liquidity to market cap ratio
            circulating_ratio: Circulating supply ratio
            holder_concentration: Holder concentration score
            market_health: Market health status
            
        Returns:
            Dictionary of trading signals
        """
        signals = {
            'liquidity_signal': 0.0,
            'volume_signal': 0.0,
            'distribution_signal': 0.0,
            'overall_signal': 0.0
        }
        
        # Liquidity signal
        if liquidity_ratio > 0.1:
            signals['liquidity_signal'] = 1.0
        elif liquidity_ratio > 0.05:
            signals['liquidity_signal'] = 0.5
        else:
            signals['liquidity_signal'] = -1.0
            
        # Volume signal
        if volume_ratio > 0.2:
            signals['volume_signal'] = 1.0
        elif volume_ratio > 0.1:
            signals['volume_signal'] = 0.5
        else:
            signals['volume_signal'] = -1.0
            
        # Distribution signal
        if holder_concentration < 0.5:
            signals['distribution_signal'] = 1.0
        elif holder_concentration < 0.7:
            signals['distribution_signal'] = 0.5
        else:
            signals['distribution_signal'] = -1.0
            
        # Overall signal based on market health
        if market_health == "healthy":
            signals['overall_signal'] = 1.0
        elif market_health == "moderate":
            signals['overall_signal'] = 0.0
        else:
            signals['overall_signal'] = -1.0
            
        return signals 